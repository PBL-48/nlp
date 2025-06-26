# 概要
## 前処理
`preprocess_data.py`で行う。
1. 課題文章群ファイルを読み込む。
   - `load_save.load_data()`で`Sentence`インスタンスに格納
     - このときは`word_list`、`polarity`は空
2. 極性辞書や自作の否定強調辞書、`janome`解析からポジネガ、品詞、否定フラグ、強調フラグ、主観／客観フラグ、経験／評価フラグ、接続助詞フラグを各単語につける。
   - `config.py`に否定、強調、主観／客観、経験／評価、接続助詞の倍率を定義しておく
     - `deny: dict[str, int]`
     - `emphasis: dict[str, int]`
     - `objectivity: dict[str, int]`
     - `experience_or_evaluation: dict[str, int]`
     - `conjunction: dict[str, int]`
   - `load_save.load_polarity_dict()`で`Token`インスタンスに格納し、`json`形式で一覧リスト`word_list`を作成
     - 途中で`config.py`を参照して後半のフィールドを埋める必要がある
     - この時点では`part_of_speech`は空
3. このような単語を並べた「文」が複数まとめられているデータが書き込まれたファイルを書き込み保存する。
   - `load_save.load_data()`で`janome`解析をし、`Token`形式で一時格納
     - このとき`word`と`part_of_speech`を埋める
     - `word_list`を参照しながら残りの欄を埋める
   - 結果をまとめて`Sentence`に格納して`json`形式で一覧リスト`sentence_list`を作成
## 本処理
`predict_polarity.py`
- **`preprocess_data.py`と同列ならファイル構造もそうした方が良いかも？**
1. 前処理ファイルを読み込む。
   - `load_preprocessed_data`
   - `sentence_list`を読み込む
2. 各単語ごとに点数計算
   - `Predict.calc_token_score()`
   - 基本ポジは1点、ネガは-1点、ニュートラルは0点。
   - 直後の単語が否定語の場合は-1倍
   - 直前の単語が強調語であれば、強調単語ごとに設定された倍率をかける。
     - **この倍率**
   - その単語が主観客観か、経験評価かによって設定された倍率をかける。
     - **この倍率**
   - 接続助詞があれば、その単語以降のポイントに一定の倍率をかける。
     - **この倍率**
3. 算出された単語の点数を各文章ごとに合算する。
   - `Predict.calc_sentence_score()`
4. これらのスコアがあらかじめ決めておいた閾値を超えればポジ、別の閾値を下回ればネガ、どちらでもなければニュートラルとする。
   - **この閾値×2**
   - `Predict.predict_polarity()`

# 詳細
## ファイル構造
```
.
├── main.py: 最初の実行ファイル
├── src/
│   ├── preprocess_data.py: 前処理をするファイル
│   └── my_library/
│       ├── config.py: 倍率やファイルパスを定義しておくファイル
│       ├── load_save.py: データの読み込み・書き込みを行うファイル
│       ├── data_models.py: データクラスを定義しておくファイル
│       └── predict_polarity.py: 点数計算やポジネガ予測を行うファイル
├── tests: ユニットテスト用ディレクトリ/
│   ├── test_load_save.py
│   ├── test_data_models.py
│   └── test_predict_polarity.py
├── requirements.txt
└── README.md
```

## 使うクラス
1. `Token`クラス
   - 単語に対応するデータクラス
   - `data_models.py`に定義
   - `@dataclass`にしておいてメソッドはなし
   - **フィールド**
     - `word: str`
     - `polarity: int (-1 or 0 or 1)`
     - `part_of_speech: str`
       - `janome`の出力結果をリストに変換
     - `not: int (-1 or 1)` or `is_not: bool`
       - デフォルトは1またはFalse
     - `emphasis: int`
       - デフォルトは1
     - `objectivity: int | None` or `is_objective: bool | None`
     - `experience_or_evaluation: int | None` or `is_evaluation: bool | None`
2. `Sentence`クラス
   - 文章に対応するデータクラス
   - `data_models.py`に定義
   - `@dataclass`にしておいてメソッドはなし
   - **フィールド**
     - `id: int`
     - `text: str`
     - `word_list: list[Token] | None`
     - `polarity: int | None`
3. `Preprocess`クラス
   - 前処理を行うクラス
   - `preprocess_data.py`に定義
   - 前処理に必要なメソッドを適宜
4. `Predict`クラス
   - 点数計算やポジネガ予測を行うクラス
   - `predict_polarity.py`に定義しておく
   - 単語の点数計算を行う`calc_token_score`メソッド
   - 文章の点数計算を行う`calc_sentence_score`メソッド
   - ポジネガ予測を行う`predict_polarity`メソッド

## 使う関数
### `config.py`内
なし
### `load_save.py`内
1. `load_data`関数
   - 課題文章群ファイルを読み込む関数
   - **引数**
     - `data: file`
   - **出力**
     - `Sentence`
2. `load_polarity_dict`関数
   - 極性辞書を読み込む関数
   - **引数**
     - `dictonary: file`
   - **出力**
     - `json`
3. `load_not_dict`関数
   - 否定辞書を読み込む関数
   - **引数**
     - なし
   - **出力**
     - `dict[str, int]`
   - **これって要るのかな？`config.py`に定義しておけば耐えそうだけど**
4. `load_emphasis_dict`関数
   - 強調辞書を読み込む関数
   - **引数**
     - なし
   - **出力**
     - `dict[str, int]`
   - **これも`config.py`に定義しておけば耐えそう**
5. `load_preprocessed_data`関数
   - 前処理済みデータを書き込む関数
   - **引数**
     - なし
   - **出力**
     - `Sentence`?
   - **これ`Predict`のメソッドに組み込んでもよさそう**