import MeCab

def func(text):

    tagger = MeCab.Tagger ("-Ochasen")
    node = tagger.parseToNode(text.encode('utf-8'))

    return text
