import pandas as pd
import sys
import os

# datatype = sys.argv[1]
WD = os.getcwd()


def make_filename(df, ndldatapath):
    direc, name = df.split('/')
    name, ext = name.split('.')
    name = ndldatapath + '_'.join(['events', name]) + '.gz'
    return name


def make_events(file, colcues, colouts, ndldatapath):
    eventfile = make_filename(file, ndldatapath)
    set = pd.read_csv(file, usecols=[colcues, colouts])
    set.rename(columns={colcues: 'cues',
                        colouts: 'outcomes'}, inplace=True)
    set = set[['cues', 'outcomes']]
    set.to_csv(eventfile, sep='\t', index=False, compression='gzip')



def make_eventfiles(datatype):
    if datatype == 'balanced':
        make_events('BalancedNDLData/train_set.gz', 'Cues', 'Aspect', 'BalancedNDLData/')
        make_events('BalancedNDLData/test_set.gz', 'Cues', 'Aspect', 'BalancedNDLData/')
    else:
        make_events('NDLData/train_set.gz', 'Cues', 'Aspect', 'NDLData/')
        make_events('NDLData/test_set.gz', 'Cues', 'Aspect', 'NDLData/')
