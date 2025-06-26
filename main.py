from my_library import (
    config as counter,
)
from my_library import (
    load_save as dictionary_loader,
)
from src.my_library import (
    load_input_data as input_loader,
)
from my_library import (
    data_models as output_manager,
)
from src.my_library import (
    predict_polarity as predictor,
)

sentence_arrays = input_loader.load("data/processed_data_v1.txt")
d1 = dictionary_loader.load("data/dictionary1.txt")
d2 = dictionary_loader.load("data/dictionary2.txt")

result = []
for sentence in sentence_arrays:
    count_statistics = counter.count(d1, d2, sentence)
    result.append(predictor.predict(count_statistics))

output_manager.output(sentence_arrays, result)
