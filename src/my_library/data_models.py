from dataclasses import dataclass, field
from typing import List, Optional

# CONJ_EFFECTの変数名は適当
from config import CONJ_EFFECT


@dataclass
class Token:
    word: str
    polarity: float
    part_of_speech: str
    not_effect_value: float = 1  # ★修正: 'not' から変更 (Python予約語との衝突回避)★
    emphasis_effect_value: float = (
        1  # ★修正: 'emphasis' から変更 (Python予約語との衝突回避)★
    )
    objectivity: Optional[float] = None
    experience_or_evaluation: Optional[int] = None


@dataclass
class Sentence:
    id: int = -1
    text: str = ""
    word_list: List[Token] = field(default_factory=list)  # word_list というフィールド名


@dataclass
class ModifiedToken(Token):
    denied_effect: float = 1.0
    emphasized_effect: float = 1.0
    conj_effect: float = 1.0
    token_score: float = 0.0

    def calc_token_score(self) -> None:
        self.token_score = (
            self.polarity
            * self.denied_effect
            * self.emphasized_effect
            * self.conj_effect
            * self.objectivity
            * self.experience_or_evaluation
        )
        return

    @classmethod
    def modify_token(
        cls,
        token: Token,
        denied_effect: float = 1.0,
        emphasized_effect: float = 1.0,
        conj_effect: float = 1.0,
    ) -> "ModifiedToken":
        return cls(
            word=token.word,
            polarity=token.polarity,
            part_of_speech=token.part_of_speech,
            not_effect_value=token.not_effect_value,
            emphasis_effect_value=token.emphasis_effect_value,
            objectivity=token.objectivity,
            experience_or_evaluation=token.experience_or_evaluation,
            denied_effect=denied_effect,
            emphasized_effect=emphasized_effect,
            conj_effect=conj_effect,
        )


@dataclass
class ModifiedSentence(Sentence):
    modified_tokens: List[ModifiedToken] = field(default_factory=list)

    @classmethod
    def modify_sentence(cls, sentence: Sentence) -> "ModifiedSentence":
        modified_tokens: List[ModifiedToken] = [
            ModifiedToken.modify_token(token) for token in sentence.word_list
        ]
        sentence_length: int = len(modified_tokens)
        conj_effect: float = 1.0
        for i in range(sentence_length):
            modified_tokens[i].conj_effect = conj_effect
            # ここはいい感じに
            if sentence.word_list[i].part_of_speech == "conjunction":
                conj_effect = CONJ_EFFECT
            if i > 0:
                modified_tokens[i].emphasized_effect = modified_tokens[
                    i - 1
                ].emphasis_effect_value
            if i < sentence_length - 1:
                modified_tokens[i].denied_effect = modified_tokens[
                    i + 1
                ].not_effect_value

        return cls(id=sentence.id, text=sentence.text, modified_tokens=modified_tokens)

    def _calc_each_token_score(self) -> None:
        for token in self.modified_tokens:
            token.calc_token_score()

    def calc_sentence_score(self) -> float:
        self._calc_each_token_score()
        sentence_score: float = 0
        for token in self.modified_tokens:
            sentence_score += token.token_score
        return sentence_score
