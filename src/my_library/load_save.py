import json
from typing import List

from src.my_library.config import (
    DATA_FILE_PATH,
    OUTPUT_FILE_PATH,
    POLARITY_DICT_PATH1,
    POLARITY_DICT_PATH2,
)
from src.my_library.data_models import Sentence, Token


def load_data(data_file: str = DATA_FILE_PATH) -> List[Sentence]:
    """課題文章群ファイルを読み込む関数"""
    sentences = []
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if line:
                    # sentence = Sentence(id=i, text=line, word_list=None, polarity=None)
                    sentence = Sentence(id=i, text=line)
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
            elements = line.strip().split("\t")
            if elements:
                elements[1] = (
                    elements[1]
                    .replace("?", "")
                    .replace("a", "e")
                    .replace("pn", "e")
                    .replace("o", "e")
                    .replace("\u3000", "e")
                    .replace("p", "1")
                    .replace("n", "-1")
                    .replace("e", "0")
                )
                while len(elements) < 4:
                    elements.append("")
                if elements[2] != "":
                    if elements[2][-1] == "観":
                        elements[3] = elements[2][-2:]
                if elements[0] not in polarity_dict:
                    polarity_dict[elements[0]] = [
                        [int(elements[1]), None, elements[3], 1, elements[0]]
                    ]
                else:
                    polarity_dict[elements[0]].append(
                        [int(elements[1]), None, elements[3], 1, elements[0]]
                    )

    with open(dictionary_file2, "r", encoding="utf-8") as f:
        for line in f:
            elements = line.strip().split("\t")
            if len(elements) < 5:
                for _ in range(5 - len(elements)):
                    elements.append("")
            elements[2] = (
                elements[0].split("（")[0].replace("ポジ", "1").replace("ネガ", "-1")
            )
            elements[3] = elements[0].split("（")[1].split("）")[0]
            elements[4] = int(0)
            for word in elements[1].split(" "):
                if word != "":
                    elements[4] += 1
                    elements.append(word)
            elements = elements[2:]
            if elements[3] not in polarity_dict:
                polarity_dict[elements[3]] = [
                    [elements[0], int(elements[1]), None, elements[2]]
                    + list(elements[3:])
                ]
            else:
                polarity_dict[elements[3]].append(
                    [elements[0], int(elements[1]), None, elements[2]]
                    + list(elements[3:])
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
