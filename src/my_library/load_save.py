from data_models import Sentence


def load_data(file_path):
    """
    課題文章群ファイルを読み込む。
    """
    sentences: list[Sentence] = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:  # 空行を無視
                sentences.append(Sentence(text=line))
    return sentences

def
