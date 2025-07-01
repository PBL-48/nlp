import os
import sys
project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root_path)
import pytest
from src.my_library.data_models import Token, Sentence, ModifiedToken, ModifiedSentence

class TestCalculator:
    # 各テストメソッドの前に実行されるセットアップ処理
    # self.calculator を初期化して、各テストで新しいインスタンスを使えるようにする
    def setup_method(self):
        token = Token(
            word="美しい",
            polarity=1.0,
            part_of_speech="noun",
            not_effect_value=1.0,
            emphasis_effect_value=1.0,
            objectivity=2.0,
            experience_or_evaluation=2.0
        )
        self.modified_token = ModifiedToken.modify_token(token)

    def test_calc_token_score(self):
        assert self.modified_token.calc_token_score() == 4.0

    # クラス全体で共有されるセットアップ処理 (オプション)
    # def setup_class(cls):
    #     print("\nSetting up TestCalculator class...")

    # クラス全体で共有されるティアダウン処理 (オプション)
    # def teardown_class(cls):
    #     print("Tearing down TestCalculator class.")

    # 各テストメソッドの後に実行されるティアダウン処理 (オプション)
    # def teardown_method(self):
    #     print(f"Teardown for {self.calculator} instance.")