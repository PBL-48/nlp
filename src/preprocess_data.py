from janome.tokenizer import Tokenizer

from my_library.data_models import Sentence, Token
from my_library.load_save import load_data


def tokenize_sentence() -> list[Sentence]:
    """
    課題文の文章を形態素解析するだけ。
    """
    return_list: list[Sentence] = []
    for sentence in load_data():
        sentence.word_list = [
            Token(
                word=token.surface,
                polarity=1,
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
