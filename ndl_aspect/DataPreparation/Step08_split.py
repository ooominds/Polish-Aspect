import pandas as pd
import os


WD = os.getcwd()


def balanced_sample(data):
    data = pd.read_csv(data)
    g = data.groupby('TA_Tags')
    subsample = g.apply(lambda x: x.sample(g.size().min()).reset_index(drop=True))
    subsample.to_csv('Data/balanced_sample.gz', index=False)


def split(datapath, ndldatapath):
    data = pd.read_csv(datapath)
    g = data.groupby('TA_Tags')
    train = g.apply(lambda x: x.sample(frac=0.8).reset_index(drop=True))
    train.to_csv(ndldatapath + 'train_set.gz', index=False)
    test = data[~data['SentenceID'].isin(train['SentenceID'].tolist())]
    test.to_csv(ndldatapath + 'test_set.gz', index=False)



def splitData(dataset_type):
    corpus = 'Data/sample.gz'
    if dataset_type == 'balanced':
        balanced_sample(corpus)
        os.mkdir('BalancedNDLData/')
        split('Data/balanced_sample.gz', 'BalancedNDLData/')
    else:
        os.mkdir('NDLData/')
        split(corpus, 'NDLData/')

