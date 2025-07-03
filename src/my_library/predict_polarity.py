from typing import List

from src.my_library.config import UNDER_THRESHOLD, UPPER_THRESHOLD
from src.my_library.data_models import ModifiedSentence, Sentence


class Predictor:
    def __init__(self, sentences: List[Sentence]):
        self.modified_sentences: List[ModifiedSentence] = [
            ModifiedSentence.modify_sentence(sentence) for sentence in sentences
        ]

    def predict_polarity(self) -> List[float]:
        """
        各文の極性を予測する。
        予測結果は、各文のスコアのリストとして返される。
        スコアは、-1.0から1.0の範囲で、負の極性、正の極性、中立を表す。
        """
        print("debug[Predictor]: point1")
        total_scores: List[float] = [
            modified_sentence.calc_sentence_score()
            for modified_sentence in self.modified_sentences
        ]
        judges: List[str] = []
        for total_score in total_scores:
            judge: str = ""
            if total_score < UNDER_THRESHOLD:
                judge = "negative"
            elif total_score > UPPER_THRESHOLD:
                judge = "positive"
            else:
                judge = "neutral"
            judges.append(judge)
        return total_scores
