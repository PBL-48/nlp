from src.my_library.data_models import ModifiedSentence
from src.my_library.load_save import save_preprocessed_data
from src.my_library.predict_polarity import Predictor
from src.preprocess_data import preprocess_data

preprocessed_sentences = preprocess_data()
save_preprocessed_data(preprocessed_sentences)
# 前処理が完了しておりpreprocessed_data.jsonが存在する場合は以下の行を上2行の代わりに実行
# preprocessed_sentences = load_preprocessed_data(output_file="data/preprocessed_data.json")
modified_sentences = [
    ModifiedSentence.modify_sentence(sentence) for sentence in preprocessed_sentences
]
# print(f"debug: {preprocessed_sentences}")
predictor = Predictor(modified_sentences)
results = predictor.predict_polarity()
