import os
import sys
project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root_path)
import src.my_library.load_save as src_ml_ls
from src.my_library.data_models import Sentence, Token

def test_load_input():
    mockid1 = "tests/mock_input_data1.txt"
    mockid2 = "tests/mock_input_data2.txt"
    with open(mockid1, "a", encoding="utf-8") as f:
        lines = """雨が降ってるから気分が落ち込む。早く晴れてほしいな。
大好きな音楽を聴くと気分が明るくなる。
新しい仕事が始まって緊張するけど、頑張りたい。
雨の日はどうしても気分が沈んでしまう。"""

        f.write(lines)
    
    #mockid2は存在しない

    #確認用
    #print(src_ml_ls.load_data(mockid1))

    assert src_ml_ls.load_data(mockid1) == [Sentence(id=1, text='雨が降ってるから気分が落ち込む。早く晴れてほしいな。', word_list=[]), Sentence(id=2, text='大好きな音楽を聴くと気分が明るくなる。', word_list=[]), Sentence(id=3, text='新しい仕事が始まって緊張するけど、頑張りたい。', word_list=[]), Sentence(id=4, text='雨の日はどうしても気分が沈んでしまう。', word_list=[])]
    assert src_ml_ls.load_data(mockid2) == []


    os.remove(mockid1)
    #os.remove(mockid2)

#確認用
#test_load_input()