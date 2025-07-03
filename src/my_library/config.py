import os

project_root_path = os.path.dirname(os.path.dirname("NLP"))
DATA_FILE_PATH = "data/data.txt"
POLARITY_DICT_PATH1 = "data/dictionary1.txt"
POLARITY_DICT_PATH2 = "data/dictionary2.txt"
OUTPUT_FILE_PATH = "data/preprocessed_data.json"
CONJ_EFFECT = 1.5
UPPER_THRESHOLD = 0.5
UNDER_THRESHOLD = -0.5
# 以下エラーを解消するための改善
EMPHASIS_EFFECT = {
    "とても": 1.5,
    "少し": 0.6,
}
EXPERIENCE_OR_EVALUATION = {
    "経験": 1.5,
    "評価": 1.5,
}
NOT_EFFECT = {
    "ない": -1.0,
}
OBJECTIVITY = {
    "客観": 1.0,
    "主観": 1.0,
}
