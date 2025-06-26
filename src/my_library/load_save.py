import json
from typing import List, Dict, Any
from data_models import Sentence, Token
from config import (
    deny, emphasis, objectivity, experience_or_evaluation, conjunction,
    DATA_FILE_PATH, POLARITY_DICT_PATH1,POLARITY_DICT_PATH2, OUTPUT_FILE_PATH
)


def load_data(data_file: str = DATA_FILE_PATH) -> List[Sentence]:
    """課題文章群ファイルを読み込む関数"""
    sentences = []
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if line:
                    sentence = Sentence(id=i, text=line, word_list=None, polarity=None)
                    sentences.append(sentence)
    except FileNotFoundError:
        print(f"Error[load_data]: {data_file}が見つからない")
        return []
    
    return sentences


def load_polarity_dict(dictionary_file1: str = POLARITY_DICT_PATH1, dictionary_file2: str = POLARITY_DICT_PATH2) -> Dict[str, int]:
    """極性辞書を読み込む関数"""
    polarity_dict = {}
    with open(dictionary_file1, 'r') as f:
        for line in f:
            line=line.strip().split('\t')
            if line:
                line[1]=line[1].replace("?","").replace("a","e").replace("pn","e").replace("o","e").replace("\u3000","e").replace("p",str(1)).replace("n",str(-1)).replace("e",str(0))
                line[1]=int(line[1])
                while len(line)<4:
                    line.append("")
                if line[2]!="":
                    if line[2][-1]=="観":
                        line[3]=line[2][-2:]
                if line[0] not in polarity_dict:
                    polarity_dict[line[0]] = [[line[1],None,line[3],1,line[0]]]
                else:
                    polarity_dict[line[0]].append([line[1],None,line[3],1,line[0]])

    with open(dictionary_file2, 'r') as f:
        for line in f:
            line=line.strip().split('\t')
            if len(line)!=2:
                continue
            else:
                for i in range(3):
                    line.append("")
            line[2]=line[0].split("（")[0]
            line[3]=line[0].split("（")[1].split("）")[0]
            line[4]=0
            for i in line[1].split(" "):
                if i=="":
                    continue
                else:
                    line[4]+=1
                    line.append(i)
            if line[2]=="ネガ":
                line[2]=-1
            elif line[2]=="ポジ":
                line[2]=1
            line=line[2:]
            if line[3] not in polarity_dict:
                polarity_dict[line[3]] = [[line[0],line[1],None,line[2]]+line[3:]]
            else:
                polarity_dict[line[3]].append([line[0],line[1],None,line[2]]+line[3:])
    return polarity_dict

