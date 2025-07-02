import json
from typing import List

from .config import (
    DATA_FILE_PATH,
    OUTPUT_FILE_PATH,
    POLARITY_DICT_PATH1,
    POLARITY_DICT_PATH2,
)
from .data_models import Sentence, Token


def load_data(data_file: str = DATA_FILE_PATH) -> List[Sentence]:
    """課題文章群ファイルを読み込む関数"""
    sentences = []
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if line:
                    # sentence = Sentence(id=i, text=line, word_list=None, polarity=None)
                    sentence = Sentence(id=i, text=line, word_list=None)
                    sentences.append(sentence)
    except FileNotFoundError:
        print(f"Error[load_data]: {data_file}が見つからない")
        return []
    print(f"実行完了[load_data]: {data_file}")
    return sentences


def load_polarity_dict(
    dictionary_file1: str = POLARITY_DICT_PATH1,
    dictionary_file2: str = POLARITY_DICT_PATH2,
) -> dict[str, list[list]]:
    """極性辞書を読み込む関数"""
    polarity_dict = {}
    with open(dictionary_file1, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip().split("\t")
            if line:
                line[1] = (
                    line[1]
                    .replace("?", "")
                    .replace("a", "e")
                    .replace("pn", "e")
                    .replace("o", "e")
                    .replace("\u3000", "e")
                    .replace("p", str(1))
                    .replace("n", str(-1))
                    .replace("e", str(0))
                )
                line[1] = int(line[1])
                while len(line) < 4:
                    line.append("")
                if line[2] != "":
                    if line[2][-1] == "観":
                        line[3] = line[2][-2:]
                if line[0] not in polarity_dict:
                    polarity_dict[line[0]] = [[line[1], None, line[3], 1, line[0]]]
                else:
                    polarity_dict[line[0]].append([line[1], None, line[3], 1, line[0]])

    with open(dictionary_file2, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip().split("\t")
            if len(line) != 2:
                continue
            else:
                for i in range(3):
                    line.append("")
            line[2] = line[0].split("（")[0]
            line[3] = line[0].split("（")[1].split("）")[0]
            line[4] = 0
            for i in line[1].split(" "):
                if i == "":
                    continue
                else:
                    line[4] += 1
                    line.append(i)
            if line[2] == "ネガ":
                line[2] = -1
            elif line[2] == "ポジ":
                line[2] = 1
            line = line[2:]
            if line[3] not in polarity_dict:
                polarity_dict[line[3]] = [[line[0], line[1], None, line[2]] + line[3:]]
            else:
                polarity_dict[line[3]].append(
                    [line[0], line[1], None, line[2]] + line[3:]
                )
    print(f"実行完了[load_polarity_dict]: {dictionary_file1}と{dictionary_file2}")
    return polarity_dict


def load_preprocessed_data(output_file: str = OUTPUT_FILE_PATH) -> List[Sentence]:
    """前処理済みデータを読み込む関数"""
    try:
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            sentences = []
            for item in data:
                sentence = Sentence(
                    id=item["id"],
                    text=item["text"],
                    word_list=[
                        Token(
                            word=token["word"],
                            polarity=token["polarity"],
                            part_of_speech=token["part_of_speech"],
                            not_effect_value=token["not_effect_value"],
                            emphasis_effect_value=token["emphasis_effect_value"],
                            objectivity=token["objectivity"],
                            experience_or_evaluation=token["experience_or_evaluation"],
                        )
                        for token in item["word_list"]
                    ],
                )
                sentences.append(sentence)
    except FileNotFoundError:
        print(f"Error[load_preprocessed_data]: {output_file}が見つからない")
        return []
    print(f"実行完了[load_preprocessed_data]: {output_file}")
    return sentences


def save_preprocessed_data(
    sentences: List[Sentence], output_file: str = OUTPUT_FILE_PATH
) -> None:
    """前処理済みデータを保存する関数"""
    data = []
    for sentence in sentences:
        data.append(
            {
                "id": sentence.id,
                "text": sentence.text,
                "word_list": [
                    {
                        "word": token.word,
                        "polarity": token.polarity,
                        "part_of_speech": token.part_of_speech,
                        "not_effect_value": token.not_effect_value,
                        "emphasis_effect_value": token.emphasis_effect_value,
                        "objectivity": token.objectivity,
                        "experience_or_evaluation": token.experience_or_evaluation,
                    }
                    for token in sentence.word_list
                ],
            }
        )
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"実行完了[save_preprocessed_data]: {output_file}")


if __name__ == "__main__":
    token = Token(
        word="こんにちは",
        polarity=1,
        objectivity=1,
        experience_or_evaluation=1,
        part_of_speech="名詞",
    )
    sentences = [
        Sentence(id=1, text="こんにちは1", word_list=[token]),
        Sentence(id=2, text="こんにちは2", word_list=[token]),
        Sentence(id=3, text="こんにちは3", word_list=[token]),
        Sentence(id=4, text="こんにちは4", word_list=[token]),
        Sentence(id=5, text="こんにちは5", word_list=[token]),
        Sentence(id=6, text="こんにちは6", word_list=[token]),
    ]
    save_preprocessed_data(sentences, OUTPUT_FILE_PATH)
    sentences_loaded = load_preprocessed_data(OUTPUT_FILE_PATH)
    print(f"セーブ前後の一致: {sentences == sentences_loaded}")
    print(f"ロードしたSentenceの１つ目: {sentences_loaded[0]}")
    print(f"ロードしたSentenceの１つ目のword_list: {sentences_loaded[0].word_list}")
    print(
        f"ロードしたSentenceの１つ目のword_listの１つ目のToken: {sentences_loaded[0].word_list[0]}"
    )
