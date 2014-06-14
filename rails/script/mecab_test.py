#-*- coding: utf-8 -*-

import MeCab
import constants
import csv
import utils
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer

MAX_DF = 0.8
MAX_FEATURES = 10000
LSA_DIM = 500

TAGS = [ "fab", "study", "ir", "hardware", "app", "business", "hci", "system", "sound" ]

def is_bigger_than_min_tfidf(term, terms, tfidfs):
    '''
    [term for term in terms if is_bigger_than_min_tfidf(term, terms, tfidfs)]で使う
    list化した、語たちのtfidfの値のなかから、順番に当てる関数。
    tfidfの値がMIN_TFIDFよりも大きければTrueを返す
    '''
    if tfidfs[terms.index(term)] > 0: #constants.MIN_TFIDF:
        return True
    return False

def tfidf(texts):
    # analyzerは文字列を入れると文字列のlistが返る関数
    vectorizer = TfidfVectorizer(analyzer=utils.analyzer, min_df=1, max_df=50)
    # corpus = [page.text for page in pages]

    x = vectorizer.fit_transform(texts)

    #  ここから下は返す値と関係ない。tfidfの高い語がどんなものか見てみたかっただけ
    terms = vectorizer.get_feature_names()
    tfidfs = x.toarray()[0]
    w = []
    for term in terms:
    	if is_bigger_than_min_tfidf(term, terms, tfidfs):
    	    value = tfidfs[terms.index(term)]
            w.append([term, value])
    filename = "script/words.csv"
    utils.write2csv(filename, w)

    print('合計%i種類の単語が%iページから見つかりました。' % (len(terms), len(texts)))

    return x, vectorizer  # xはtfidf_resultとしてmainで受け取る

def func(texts):

    tfidf_result, vectorizer = tfidf(texts)  # tfidf_resultはtfidf関数のx
    # print tfidf_result

    # dimensionality reduction by LSA
    # lsa = TruncatedSVD(LSA_DIM)
    # x = lsa.fit_transform(tfidf_result)
    # x = Normalizer(copy=False).fit_transform(x)
    # print x

    return True
