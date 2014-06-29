#-*- coding: utf-8 -*-

import MeCab
import constants
import csv
import os
import utils
import re
import tag
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB

MAX_DF = 0.8
MAX_FEATURES = 10000
LSA_DIM = 500

TRAIN_DATA_CONTENT_FILE_PATH = 'public/data/train_data_content.csv'
TRAIN_DATA_TAG_FILE_PATH = 'public/data/train_data_tag.csv'
TEST_DATA_CONTENT_FILE_PATH = 'public/data/test_data_content.csv'
TEST_DATA_TAG_FILE_PATH = 'public/data/test_data_tag.csv'

TAGS = [ "fab", "study", "ir", "hardware", "app", "business", "hci", "system", "sound" ]

def is_bigger_than_min_tfidf(term, terms, tfidfs):
    '''
    [term for term in terms if is_bigger_than_min_tfidf(term, terms, tfidfs)]で使う
    list化した、語たちのtfidfの値のなかから、順番に当てる関数。
    tfidfの値がMIN_TFIDFよりも大きければTrueを返す
    '''
    # if tfidfs[terms.index(term)] > constants.MIN_TFIDF:
    if tfidfs[terms.index(term)] > 0:
        return True
    return False

def tfidf(texts):
    # analyzerは文字列を入れると文字列のlistが返る関数
    # vectorizer = TfidfVectorizer(analyzer=utils.stems, min_df=1, max_df=50)
    vectorizer = TfidfVectorizer(analyzer=utils.analyzer, min_df=1, max_df=1.0/(len(TAGS)+1))

    x = vectorizer.fit_transform(texts)

    # utils.write2csv('script/stop_words.csv', vectorizer.get_stop_words().toarray())
    print vectorizer.get_stop_words()

    #  ここから下は返す値と関係ない。tfidfの高い語がどんなものか見てみたかっただけ
    filename = "script/words.csv"
    terms = vectorizer.get_feature_names()
    tfidfs = x.toarray()[0]
    w = []
    for term in terms:
    	if is_bigger_than_min_tfidf(term, terms, tfidfs):
    	    value = tfidfs[terms.index(term)]
            # utils.append2file(filename, term + ',' + str(value) + os.linesep)
            w.append([term, value])
    utils.write2csv(filename, w)

    print('合計%i種類の単語が%iページから見つかりました。' % (len(terms), len(texts)))

    return x, vectorizer  # xはtfidf_resultとしてmainで受け取る

def func(texts):

    contents = []
    f = open(TRAIN_DATA_CONTENT_FILE_PATH, 'r')
    for line in f:
        line = re.sub('，|‘|’|　|、|。|「|」', '', line)
        line = re.sub('/\\/', '', line)
        contents.append(line)
    f.close()

    tfidf_result, vectorizer = tfidf(contents)  # tfidf_resultはtfidf関数のx
    utils.write2csv('script/result.csv', tfidf_result.toarray())

    # dimensionality reduction by LSA
    # lsa = TruncatedSVD(LSA_DIM)
    # x = lsa.fit_transform(tfidf_result)
    # x = Normalizer(copy=False).fit_transform(x)
    # print x

    # print tag.train_tags()

    data = tfidf_result.toarray()
    target = tag.train_tags()

    gnb = GaussianNB()
    bnb = BernoulliNB()

    # for i, text in enumerate(texts):
    #     texts[i] = re.sub('，|‘|’|　|、|。|「|」| |', '', text)
    #     texts[i] = re.sub('/\\/|/\t/', '', text)

    contents = []
    f = open(TEST_DATA_CONTENT_FILE_PATH, 'r')
    for line in f:
        line = re.sub('，|‘|’|　|、|。|「|」', '', line)
        line = re.sub('/\\/', '', line)
        contents.append(line)
    f.close()

    print 'tfidf fitting for test contents'
    test_contents = vectorizer.transform(contents)
    print 'toarray'
    x = test_contents.toarray()
    print 'data len'
    print len(data[0])
    print 'test len'
    print len(x[0])

    print 'GaussianNB calicurating...'
    y_pred_gnb = gnb.fit(data, target).predict(x)
    y_pred_bnb = bnb.fit(data, target).predict(x)
    # print("Number of mislabeled points : %d" % (iris.target != y_pred).sum())
    # print y_pred

    for i, y in enumerate(y_pred_gnb):
        print 'gnb:' + tag.value(y_pred_gnb[i])
        print 'bnb:' + tag.value(y_pred_bnb[i])
        print contents[i][0:200]

    return True
