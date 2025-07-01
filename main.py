from src.my_library.load_save import load_preprocessed_data
from src.my_library.data_models import ModifiedSentence
from src.my_library.predict_polarity import Predictor

sentences = load_preprocessed_data()
modified_sentences = [ModifiedSentence.modify_sentence(sentence) for sentence in sentences]
predictor = Predictor(modified_sentences)
results = predictor.predict_polarity()
print(results)
