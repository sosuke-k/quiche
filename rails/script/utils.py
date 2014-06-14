#-*- coding: utf-8 -*-

import MeCab
import csv
import constants

def write2csv(filename, texts):
    writecsv = csv.writer(file(filename, 'w'), lineterminator="""
""") # 書き込みファイルの設定
    writecsv.writerows(texts) # 複数行(リストのリスト|テーブル)の書き込み
    return True

def analyzer(text):
    ret = []
    tagger = MeCab.Tagger('-Ochasen')
    node = tagger.parseToNode(text)
    node = node.next
    while node.next:
        ret.append(node.feature.split(',')[-3])
        node = node.next

    return ret

def _split_to_words(text, to_stem=False):
    """
    入力: 'すべて自分のほうへ'
    出力: tuple(['すべて', '自分', 'の', 'ほう', 'へ'])
    """
    tagger = MeCab.Tagger('mecabrc')  # 別のTaggerを使ってもいい
    mecab_result = tagger.parse(text)
    info_of_words = mecab_result.split('\n')
    words = []
    for info in info_of_words:
        # macabで分けると、文の最後に’’が、その手前に'EOS'が来る
        if info == 'EOS' or info == '':
            break
            # info => 'な\t助詞,終助詞,*,*,*,*,な,ナ,ナ'
        info_elems = info.split(',')
        # 6番目に、無活用系の単語が入る。もし6番目が'*'だったら0番目を入れる
        if info_elems[6] == '*':
            # info_elems[0] => 'ヴァンロッサム\t名詞'
            words.append(info_elems[0][:-3])
            continue
        if to_stem:
            # 語幹に変換
            words.append(info_elems[6])
            continue
        # 語をそのまま
        words.append(info_elems[0][:-3])
    return words

def words(text):
    words = _split_to_words(text=text, to_stem=False)
    return words

def stems(text):
    stems = _split_to_words(text=text, to_stem=True)
    return stems
