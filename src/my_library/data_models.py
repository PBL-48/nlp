from dataclasses import dataclass, field
from typing import List, Optional, Self

from config import CONJ_EFFECT


@dataclass
class Token:
    word: str
    polarity: float
    part_of_speech: str
    not_effect_value: float = 1.0  # ★修正: 'not' から変更 (Python予約語との衝突回避)★
    emphasis_effect_value: float = (
        1.0  # ★修正: 'emphasis' から変更 (Python予約語との衝突回避)★
    )
    objectivity: Optional[float] = None
    experience_or_evaluation: Optional[float] = None

    def __str__(self: Self) -> str:
        return self.word


@dataclass
class Sentence:
    id: int = -1
    text: str = ""
    word_list: List[Token] = field(default_factory=list)  # word_list というフィールド名

    def __str__(self: Self):
        return self.text


@dataclass
class ModifiedToken(Token):
    denied_effect: float = 1.0
    emphasized_effect: float = 1.0
    conj_effect: float = 1.0
    token_score: float = 0.0

    def calc_token_score(self: Self) -> None:
        print(type(self.polarity))
        print(type(self.denied_effect))
        print(type(self.emphasized_effect))
        print(type(self.conj_effect))
        print(type(self.objectivity))
        print(type(self.experience_or_evaluation))
        self.token_score = (
            self.polarity
            * self.denied_effect
            * self.emphasized_effect
            * self.conj_effect
            # * (self.objectivity if self.objectivity is not None and self.objectivity != '' else 1.0)
            # * (self.experience_or_evaluation if self.experience_or_evaluation is not None and self.experience_or_evaluation != '' else 1.0)
        )
        print(f"debug[ModifiedToken]: [{self.word}] {self.token_score}]")
        print(
            f"debug[ModifiedToken]: [{self.polarity}] [{self.denied_effect}] [{self.emphasized_effect}] [{self.conj_effect}] [{self.objectivity}] [{self.experience_or_evaluation}]"
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
        # print(f"debug[ModifiedToken]: point6{token}")#正常
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
        # print(f"debug[ModifiedSentence]: point5{modified_tokens}")
        print("debug[ModifiedSentence]: point5")
        sentence_length: int = len(modified_tokens)
        conj_effect: float = 1.0
        for i in range(sentence_length):
            modified_tokens[i].conj_effect = conj_effect
            if sentence.word_list[i].part_of_speech in ["接続詞", "接続助詞"]:
                conj_effect = CONJ_EFFECT
            if i > 0:
                modified_tokens[i].emphasized_effect = modified_tokens[
                    i - 1
                ].emphasis_effect_value
            if i < sentence_length - 1:
                modified_tokens[i].denied_effect = modified_tokens[
                    i + 1
                ].not_effect_value

        return cls(
            id=sentence.id,
            text=sentence.text,
            word_list=sentence.word_list,
            modified_tokens=modified_tokens,
        )

    def _calc_each_token_score(self) -> None:
        for token in self.modified_tokens:
            token.calc_token_score()

    def calc_sentence_score(self) -> float:
        print(f"debug[ModifiedSentence]: point2[{self}]")
        self._calc_each_token_score()
        sentence_score: float = 0
        print(f"debug[ModifiedSentence]: point8[{self.word_list}]")
        print(f"debug[ModifiedSentence]: point3{self.modified_tokens}")
        for token in self.modified_tokens:
            print(f"debug[ModifiedSentence]: point4[{token.token_score}]")
            sentence_score += token.token_score
        return sentence_score
