import os

project_root_path = os.path.dirname(os.path.dirname("NLP"))
DATA_FILE_PATH = "data/data.txt"
POLARITY_DICT_PATH1 = "data/dictionary1.txt"
POLARITY_DICT_PATH2 = "data/dictionary2.txt"
OUTPUT_FILE_PATH = "data/preprocessed_data.json"
CONJ_EFFECT = 1.5
UPPER_THRESHOLD = 0.5
UNDER_THRESHOLD = -0.5
NOT_EFFECT = {"ない": -1.0}
EMPHASIS_EFFECT = {
    "とても": 2.0,
    "一番": 3.0,
    "どうしても": 2.0,
    "最高": 3.0,
    "少し": 0.5,
    "なかなか": 1.5,
    "特に": 2.0,
    "久しぶり": 1.3,
    "ずっと": 1.3,
    "一日中": 1.3,
    "早く": 1.3,
    "いっぱい": 1.3,
    "たくさん": 1.3,
}
