from data_models import Token, Sentence, ModifiedToken, ModifiedSentence
# 閾値の変数名は適当
from config import UNDER_THRESHOLD, UPPER_THRESHOLD

class Predictor():
    def __init__(self, sentence: Sentence):
        self.modified_sentence = ModifiedSentence.modify_sentence(sentence)

    def predict_polarity(self) -> str:
        total_score = self.modified_sentence.calc_sentence_score()
        if total_score < UNDER_THRESHOLD:
            return "negative"
        elif total_score > UPPER_THRESHOLD:
            return "positive"
        else:
            return "neutral"
