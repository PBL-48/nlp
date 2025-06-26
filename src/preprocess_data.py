from janome.tokenizer import Tokenizer

from my_library.data_models import Token
from my_library.load_save import load_data


def preprocess_data():
    for sentence in load_data():
        sentence.word_list = [
            Token(
                word=token.surface,
                polarity=None,
                part_of_speech=token.part_of_speech.split(","),
                not_effect_value=None,
                emphasis_effect_value=None,
                objectivity=None,
                experience_or_evaluation=None,
            )
            for token in Tokenizer().tokenize(sentence.text)
        ]
