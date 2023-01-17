import os
import numpy as np
import pandas as pd

WD = os.getcwd()

FREQ_1G_PATH = 'Data/1gram.csv'
FREQ_2G_PATH = 'Data/2gram.csv'
FREQ_3G_PATH = 'Data/3gram.csv'
FREQ_4G_PATH = 'Data/4gram.gz'
# Final list of ngrams to use in training (5000)
TARGETS = "Data/ngrams_to_use.csv"
# Separate lists of chunks
TARGETS_1G = "Data/1grams_touse.csv"
TARGETS_2G = "Data/2grams_touse.csv"
TARGETS_3G = "Data/3grams_touse.csv"
TARGETS_4G = "Data/4grams_touse.csv"
ALL_CUES = 'Data/all_cues_to_use.csv'
LEMMAS = 'Data/superlemmas.csv'
TENSES = 'DownloadedData/all_tenses.csv'

N = 10000


def prepare_all_cues():
    # Load as dataframe and retain only 10k ngrams whose freq >= 10
    Freq_1G_df = pd.read_csv(FREQ_1G_PATH)
    Freq_1G_df.dropna(inplace=True)  # Remove the row corresponding to the empty n-gram
    Freq_1G_df = Freq_1G_df[Freq_1G_df['frequency'] >= 10]  # Remove ngrams whose freq < 10
    Freq_1G_df = Freq_1G_df.sample(frac=1)  # Shuffle ngrams with the same frequency
    Freq_1G_df = Freq_1G_df.sort_values(by=['frequency'], ascending=False).reset_index(
        drop=True)  # Sort in a descending order by the frequency
    Freq_1G_df = Freq_1G_df.iloc[0:N]  # Extract N ngrams

    ########## 2-grams ##########
    # Load as dataframe and retain only 10k ngrams whose freq >= 10
    Freq_2G_df = pd.read_csv(FREQ_2G_PATH)
    Freq_2G_df.dropna(inplace=True)  # Remove the row corresponding to the empty n-gram
    Freq_2G_df = Freq_2G_df[Freq_2G_df['frequency'] >= 10]  # Remove ngrams whose freq < 10
    Freq_2G_df = Freq_2G_df.sample(frac=1)  # Shuffle ngrams with the same frequency
    Freq_2G_df = Freq_2G_df.sort_values(by=['frequency'], ascending=False).reset_index(
        drop=True)  # Sort in a descending order by the frequency
    Freq_2G_df = Freq_2G_df.iloc[0:N]  # Extract N ngrams

    ########## 3-grams ##########
    # Load as dataframe and retain only 10k ngrams whose freq >= 10
    Freq_3G_df = pd.read_csv(FREQ_3G_PATH)
    Freq_3G_df.dropna(inplace=True)  # Remove the row corresponding to the empty n-gram
    Freq_3G_df = Freq_3G_df[Freq_3G_df['frequency'] >= 10]  # Remove ngrams whose freq < 10
    Freq_3G_df = Freq_3G_df.sample(frac=1)  # Shuffle ngrams with the same frequency
    Freq_3G_df = Freq_3G_df.sort_values(by=['frequency'], ascending=False).reset_index(
        drop=True)  # Sort in a descending order by the frequency
    Freq_3G_df = Freq_3G_df.iloc[0:N]  # Extract N ngrams

    ########## 4-grams ##########
    # Load as dataframe and retain only 10k ngrams whose freq >= 10
    Freq_4G_df = pd.read_csv(FREQ_4G_PATH)
    Freq_4G_df.dropna(inplace=True)  # Remove the row corresponding to the empty n-gram
    Freq_4G_df = Freq_4G_df[Freq_4G_df['frequency'] >= 10]  # Remove ngrams whose freq < 10
    Freq_4G_df = Freq_4G_df.sample(frac=1)  # Shuffle ngrams with the same frequency
    Freq_4G_df = Freq_4G_df.sort_values(by=['frequency'], ascending=False).reset_index(
        drop=True)  # Sort in a descending order by the frequency
    Freq_4G_df = Freq_4G_df.iloc[0:N]  # Extract N ngrams

    ########## All n-grams ##########
    # Append all datasets

    Freq_all_df = Freq_1G_df.copy()
    Freq_all_df = Freq_all_df.append([Freq_2G_df.copy(), Freq_3G_df.copy(), Freq_4G_df.copy()])

    # Save a separate dataframe for each group
    Freq_1G_df.to_csv(TARGETS_1G, sep=',', index=False)
    Freq_2G_df.to_csv(TARGETS_2G, sep=',', index=False)
    Freq_3G_df.to_csv(TARGETS_3G, sep=',', index=False)
    Freq_4G_df.to_csv(TARGETS_4G, sep=',', index=False)
    Freq_all_df.to_csv(TARGETS, sep=',', index=False)

    ngrams = pd.read_csv(TARGETS)
    ngrams.drop(columns=['frequency'], inplace=True)

    infinitives = pd.read_csv(LEMMAS, header=None, names=["lemmas"])
    infinitives['lemmas'] = infinitives['lemmas'].apply(lambda s: s.upper())

    ngrams.rename(columns={'ngram': 'cue'}, inplace=True)
    infinitives.rename(columns={'lemmas': 'cue'}, inplace=True)
    tenses = pd.read_csv(TENSES)
    tenses.to_csv('Data/all_tenses_to_use.csv', index=False, header=False)
    tenses.drop(columns=['index'], inplace=True)
    # all_cues_df = infinitives_df.copy()
    all_cues_df = ngrams.copy()
    all_cues_df = all_cues_df.append([infinitives.copy(), tenses.copy()])

    all_cues_df['index'] = np.arange(1, (len(all_cues_df) + 1))

    all_cues_df.to_csv(ALL_CUES, sep=',', index=False, header=False)

    all_lemmas_df = infinitives.copy()
    all_lemmas_df['index'] = np.arange(1, (len(all_lemmas_df) + 1))
    ALL_LEMMAS = 'Data/all_superlemmas_to_use.csv'
    all_lemmas_df.to_csv(ALL_LEMMAS, sep=',', index=False, header=False)
    ngram_df = ngrams.copy()
    ngram_df['index'] = np.arange(1, len(ngram_df) + 1)
    ALL_NGRAMS = 'Data/all_ngrams_to_use.csv'
    ngram_df.to_csv(ALL_NGRAMS, sep=',', index=False, header=False)

    ngram_tense = ngrams.copy()
    ngram_tense = ngram_tense.append(tenses.copy())
    ngram_tense['index'] = np.arange(1, len(ngram_tense) + 1)
    NGRAM_TENSE = 'Data/ngrams_tenses_to_use.csv'
    ngram_tense.to_csv(NGRAM_TENSE, index=False, header=False)

    lemma_tenses = infinitives.copy()
    lemma_tenses = lemma_tenses.append(tenses.copy())
    lemma_tenses['index'] = np.arange(1, len(lemma_tenses) + 1)
    LEMMA_TENSE = 'Data/superlemmas_tenses_to_use.csv'
    lemma_tenses.to_csv(LEMMA_TENSE, index=False, header=False)

    ngrams_lemmas = infinitives.copy()
    ngrams_lemmas = ngrams_lemmas.append(ngrams.copy())
    ngrams_lemmas['index'] = np.arange(1, len(ngrams_lemmas) + 1)
    NGRAMS_LEMMAS = 'Data/ngrams_superlemmas_to_use.csv'
    ngrams_lemmas.to_csv(NGRAMS_LEMMAS, index=False, header=False)