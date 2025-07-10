import os
import sys
project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root_path)
import src.my_library.load_save as src_ml_ls

def test_load_dictionary():#やり方わからなかったのでたぶん処理済み辞書データに関して破壊的
    mockpd1 = "tests/mock_pol_dict1.txt"
    mockpd2 = "tests/mock_pol_dict2.txt"
    #test_result_txt = "tests/test_load_dictionary_result.txt"
    with open(mockpd2, "a", encoding="utf-8") as f:
        lines = """ネガ（経験）	あがく
ネガ（評価）	ウド の 大木 と
ポジ（経験）	移す こと は できる
ポジ（経験）	移す こと が できる
ポジ（評価）	歴々 だ"""

        f.write(lines)
    
    with open(mockpd1, "a", encoding="utf-8") as f:
        lines = """クリスマスプレゼント	p	〜がある・高まる（存在・性質）
敏感	?p?n	〜である・になる（状態）客観 & ?〜である・になる（状態）主観
豊か	p	〜である・になる（評価・感情）主観 & !〜である・になる（評価・感情）客観もあり？
最小限	n	〜である・になる（状態）客観
克明	e	〜である・になる（評価・感情）主観
安全運転	e	〜する（行為）
酵素	pn	〜する（評価・感情）客観
酵素	o	〜がある・高まる（状態）主観
酵素	a	存在・もの・名称""" #最後3行は検証用のウソ辞書 残りは元のから

        f.write(lines)

    test_result = src_ml_ls.load_polarity_dict(mockpd1,mockpd2)

    #with open(test_result_txt, "a", encoding="utf-8") as f: #人間の確認用
        #f.write(str(test_result))
    #assert src_ml_ls.load_polarity_dict(mockpd1,mockpd2) == {'クリスマスプレゼント': [[1, None, '', 1, 'クリスマスプレゼント']], '敏感': [[0, None, '主観', 1, '敏感']], '豊か': [[1, None, '', 1, '豊か']], '最小限': [[-1, None, '客観', 1, '最小限']], '克明': [[0, None, '主観', 1, '克明']], '安全運転': [[0, None, '', 1, '安全運転']], 'あがく': [[-1, '経験', None, 1, 'あがく']], 'ウド': [[-1, '評価', None, 4, 'ウド', 'の', '大木', 'と']], '移す': [[1, '経験', None, 4, '移す', 'こと', 'は', 'できる']], '歴々': [[1, '評価', None, 2, '歴々', 'だ']]}
    assert test_result['クリスマスプレゼント'] == [[1, None, '', 1, 'クリスマスプレゼント']]
    assert test_result['敏感'] == [[0, None, '主観', 1, '敏感']]
    assert test_result['豊か'] == [[1, None, '', 1, '豊か']]
    assert test_result['最小限'] == [[-1, None, '客観', 1, '最小限']]
    assert test_result['克明'] == [[0, None, '主観', 1, '克明']]
    assert test_result['安全運転'] == [[0, None, '', 1, '安全運転']]
    assert test_result['あがく'] == [[-1, '経験', None, 1, 'あがく']]
    assert test_result['ウド'] == [[-1, '評価', None, 4, 'ウド', 'の', '大木', 'と']]
    assert test_result['歴々'] == [[1, '評価', None, 2, '歴々', 'だ']]
    assert test_result['移す'][0] == [1, '経験', None, 4, '移す', 'こと', 'は', 'できる']
    assert test_result['移す'][1] == [1, '経験', None, 4, '移す', 'こと', 'が', 'できる']
    assert test_result['酵素'][0] == [0, None, '客観', 1, '酵素']
    assert test_result['酵素'][1] == [0, None, '主観', 1, '酵素']
    assert test_result['酵素'][2] == [0, None, '', 1, '酵素']



    os.remove(mockpd1)
    os.remove(mockpd2)
#確認用
#test_load_dictionary()