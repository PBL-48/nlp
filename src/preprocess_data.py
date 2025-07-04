from janome.tokenizer import Tokenizer  # type: ignore

from src.my_library.config import (
    EMPHASIS_EFFECT,
    NOT_EFFECT,
)
from src.my_library.data_models import Sentence, Token
from src.my_library.load_save import load_data, load_polarity_dict


def tokenize_sentence() -> list[Sentence]:
    """
    課題文の文章を形態素解析するだけ。
    """
    return_list: list[Sentence] = []
    for sentence in load_data():
        sentence.word_list = [
            Token(
                word=token.base_form,
                polarity=0,
                part_of_speech=token.part_of_speech.split(","),
                not_effect_value=1,
                emphasis_effect_value=1,
                objectivity=1,
                experience_or_evaluation=1,
            )
            for token in Tokenizer().tokenize(sentence.text)
        ]
        return_list.append(sentence)
    return return_list


def get_words_info(sentence: Sentence) -> Sentence:
    """辞書にある情報を入力する。"""
    polarity_dict = load_polarity_dict()
    word_list = sentence.word_list
    i = 0
    while i < len(word_list):
        applied = False
        for _, values in polarity_dict.items():
            for value in values:
                seq_len = value[3] if isinstance(value[3], int) else 1
                seq_len = max(seq_len, 1)
                if i + seq_len > len(word_list):
                    continue
                match = True
                for j in range(seq_len):
                    if word_list[i + j].word != value[4 + j]:
                        match = False
                        break
                if match:
                    word_list[i].polarity = value[0]
                    word_list[i].experience_or_evaluation = value[1]
                    word_list[i].objectivity = value[2]
                    applied = True
                    break
            if applied:
                break
        if applied:
            i += seq_len
        else:
            i += 1
    return sentence


def get_config_data(sentence: Sentence) -> Sentence:
    """config.pyに記載の内容を入力する。"""
    for token in sentence.word_list:
        if token.word in NOT_EFFECT and token.experience_or_evaluation not in [
            "経験",
            "評価",
        ]:
            # dictionary1の場合にのみ適用
            token.not_effect_value = NOT_EFFECT[token.word]
        if token.word in EMPHASIS_EFFECT:
            token.emphasis_effect_value = EMPHASIS_EFFECT[token.word]
    return sentence


def preprocess_data() -> list[Sentence]:
    """結果的にはこれを実行すればよい。"""
    return [
        get_config_data(get_words_info(sentence)) for sentence in tokenize_sentence()
    ]
