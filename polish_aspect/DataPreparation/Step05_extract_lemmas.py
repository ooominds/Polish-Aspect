import os
import pandas as pd
import pickle

WD = os.getcwd()


def extract_lemmas():
    sents = pd.read_csv(WD + 'Data/sample.gz')

    cooc_freqs = sents.groupby(["SuperLemmas", "TA_Tags"]).size().reset_index(name="Freq")
    print(cooc_freqs.shape)

    cooc_freqs = pd.crosstab(sents["SuperLemmas"], sents['TA_Tags'])
    print(cooc_freqs.shape)

    tense_col_names = list(map(lambda s: "_".join([s.replace('.', '_'), "freq"]), cooc_freqs.columns))
    cooc_freqs.columns = tense_col_names
    print(cooc_freqs.head())

    cooc_freqs['total_freq'] = cooc_freqs.sum(axis=1)

    columns_prop = list(map(lambda s: s.replace('_freq', '_prop'), tense_col_names))
    cooc_freqs = cooc_freqs.reindex(columns=cooc_freqs.columns.tolist() + columns_prop)

    for col_name in columns_prop:
        cooc_freqs[col_name] = cooc_freqs[col_name.replace('_prop', '_freq')] / cooc_freqs['total_freq']

    infinitives = cooc_freqs.index.to_frame()

    ### Export the co-occurence and infinitives datasets
    cooc_freqs.to_csv(WD + 'Data/coocc_freq_superlemmas.csv', sep=',')
    infinitives.to_csv(WD + 'Data/superlemmas.csv', sep=',', header=False, index=False)
