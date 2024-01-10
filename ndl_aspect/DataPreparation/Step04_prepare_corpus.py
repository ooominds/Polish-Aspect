import pandas as pd
from nltk.util import ngrams
import os
import gc
import pickle
from sklearn.model_selection import train_test_split

WD = os.getcwd()
TAGGED = WD + '/Data/tagged_with_sie.gz'
CORPUS = WD + '/Data/complete_corpus.gz'
SAMPLE = WD + '/Data/sample.gz'
PAIRS = WD + '/ndl_aspect/DataPreparation/DownloadedData/aspectual_pairs.pickle'


def retrieve_superlemma(inf, pairs):
    if inf in pairs:
        return pairs[inf]
    else:
        return 'NULL'


def remove_punc_generator(string):
    punc = '''”„–…!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for ele in string:
        if ele in punc:
            string = string.replace(ele, "")
            string = string.replace("  ", " ")
        if not ele.isalpha() and ele != " ":
            string = string.replace(ele, "")
            string = string.replace("  ", " ")
    yield string


def extract_context(sent, pos):
    words = sent.split()
    pos = str(pos)
    if len(pos.split()) == 1:
        pos = int(float(pos))
        context = words[:pos] + words[pos:]
    else:
        p1, p2 = pos.split()
        p1, p2 = int(float(p1)), int(float(p2))
        context = words[:p1 - 1] + words[p1:p2 - 1] + words[p2:]
    context = ' '.join(context)
    return next(remove_punc_generator(context))


def create_ngram_cues(s, n, sep_s=" ", sep_words="#", sep_ngrams='_'):
    if type(s) == str:
        words = [w for w in s.split(sep_s) if w != ""]
        s_ngrams = []
        for i in range(1, n + 1):
            s_ngrams.extend(list(ngrams(words, i)))
        return sep_ngrams.join([sep_words.join(ngram) for ngram in s_ngrams])

def split_ta(ta):
    return pd.Series(ta.split(".", 1))

def prepare():
    with open(PAIRS, 'rb') as file:
        pairs = pickle.load(file)

    tagged = pd.read_csv(TAGGED)
    tagged['SuperLemmas'] = tagged['infinitive'].apply(lambda x: retrieve_superlemma(x, pairs))
    tagged = tagged[tagged.SuperLemmas != 'NULL']
    tagged.to_csv(CORPUS, index=False)

    corpus = pd.read_csv(CORPUS)
    corpus, _ = train_test_split(corpus, train_size=10000000, stratify=corpus[['infinitive']])
    corpus.to_csv(SAMPLE, index=False)

    corpus = pd.read_csv(SAMPLE)
    corpus['Context'] = corpus.apply(lambda x: extract_context(x.loc['Sentence'], x.loc['position']), axis=1)
    corpus['SkipgramCues'] = corpus['Context'].apply(lambda s: create_ngram_cues(s, n=4, sep_s=" "))
    corpus.to_csv(SAMPLE, index=False)
    corpus = corpus[~corpus['SkipgramCues'].isnull()]
    corpus.to_csv(SAMPLE, index=False)
    gc.collect()
    corpus[['Aspect', 'Tense']] = corpus['TA_Tags'].apply(split_ta)
    # corpus = corpus[corpus.SuperLemmas != 'NULL']
    corpus['Cues'] = corpus.apply(lambda x: '_'.join([x.loc['SkipgramCues'], x.loc['SuperLemmas'], x.loc['Tense'].upper()]),
                                  axis=1)
    corpus.drop(columns=['SkipgramCues', 'Context'], inplace=True)
    print('length after skipgrams:')
    print(len(corpus))
    corpus.to_csv(SAMPLE, index=False)
