DATA_FILE_PATH = "NLP/data/data.txt"
POLARITY_DICT_PATH1 = "NLP/data/polarity_dict1.txt"
POLARITY_DICT_PATH2 = "NLP/data/polarity_dict2.txt"
OUTPUT_FILE_PATH = "NLP/data/preprocessed_data.json"
CONJ_EFFECT = 1.5
UPPER_THRESHOLD = 0.5
UNDER_THRESHOLD = -0.5
dict_not = {
    "ない": -1.0
}
dict_emphasis = {
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
    "たくさん": 1.3
}