import gc
import pandas as pd
from nltk.util import ngrams
from pyndl.count import cues_outcomes
import gzip
import os

WD = os.getcwd()
TEMP_DIR = 'TempData'
isExist = os.path.exists(TEMP_DIR)
if not isExist:
    os.mkdir('TempData')
#NUM_THREADS = 4


def remove_punc_generator(string):
    punc = '''”„–…!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for ele in string:
        if ele in punc:
            string = string.replace(ele, "")
            string = string.replace("  ", " ")
        if ele.isnumeric() and ele != " ":
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
        context = words[:p1-1] + words[p1:p2-1] + words[p2:]
    context = ' '.join(context)
    return next(remove_punc_generator(context))

def create_ngram_cues(s, n, sep_s = " ", sep_words = "#", sep_ngrams = '_'):
    words = [w for w in s.split(sep_s) if w != ""]

    s_ngrams = []
    s_ngrams.extend(list(ngrams(words, n)))

    return sep_ngrams.join([sep_words.join(ngram) for ngram in s_ngrams])


def create_ngram_event_df_file(df, n, sep_words="#"):
    df_new = df.copy()
    df_new['cues'] = df_new.apply(lambda x: create_ngram_cues(x.loc['cues'], n=n, sep_s=" "), axis=1)
    return df_new


def df_to_gz(data, gz_outfile):
    with gzip.open(gz_outfile, 'wt', encoding='utf-8') as out:
        data.to_csv(out, sep='\t', index=False)


def compute_cue_freqs(data, temp_dir, num_threads, verbose=False):
    if isinstance(data, str):
        events_path = data
    elif isinstance(data, pd.DataFrame):
        events_path = os.path.join(temp_dir, 'events_temp.gz')
        df_to_gz(data=data, gz_outfile=events_path)
    else:
        raise ValueError("data should be either a path to an event file or a dataframe")
    n_events, cue_freqs, outcome_freqs = cues_outcomes(events_path,
                                                       number_of_processes=num_threads,
                                                       verbose=verbose)
    cue_freqs_df = pd.DataFrame(cue_freqs.most_common())
    cue_freqs_df.columns = ['ngram', 'frequency']
    cue_freqs_df = cue_freqs_df[cue_freqs_df.ngram != '']
    gc.collect()

    return cue_freqs_df


def extract_ngrams(NUM_THREADS):
    sents = pd.read_csv('Data/sample.gz')
    sents['Context'] = sents.apply(lambda x: extract_context(x.loc['Sentence'], x.loc['position']), axis=1)
    sents = sents.rename(columns={"Context":"cues", "Aspect": "outcomes"})
    sents = sents[["cues", "outcomes"]]
    sents_1gram = create_ngram_event_df_file(sents, 1, sep_words="#")
    ngram_freqs1 = compute_cue_freqs(sents_1gram, TEMP_DIR, NUM_THREADS, verbose=True)
    #len(ngram_freqs1[ngram_freqs1['frequency'] >= 10])
    ngram_freqs1.to_csv('Data/1gram.csv', sep=',', index=False)
    del ngram_freqs1, sents_1gram
    gc.collect()
    sents_2gram = create_ngram_event_df_file(sents, 2, sep_words="#")
    ngram_freqs2 = compute_cue_freqs(sents_2gram, TEMP_DIR, NUM_THREADS, verbose=True)
    #len(ngram_freqs2[ngram_freqs2['frequency'] >= 10])
    ngram_freqs2.to_csv('Data/2gram.csv', sep=',', index=False)
    del ngram_freqs2, sents_2gram
    gc.collect()


    sents_3gram = create_ngram_event_df_file(sents, 3, sep_words="#")
    ngram_freqs3 = compute_cue_freqs(sents_3gram, TEMP_DIR, NUM_THREADS, verbose=True)
    #len(ngram_freqs3[ngram_freqs3['frequency'] >= 10])
    ngram_freqs3.to_csv('Data/3gram.csv', sep=',', index=False)
    del ngram_freqs3, sents_3gram
    gc.collect()

    sents_4grams = create_ngram_event_df_file(sents, 4, sep_words="#")
    ngram_freqs4 = compute_cue_freqs(sents_4grams, TEMP_DIR, NUM_THREADS, verbose=True)
    #len(ngram_freqs4[ngram_freqs4['frequency'] >= 10])
    ngram_freqs4.to_csv('Data/4gram.gz', sep=',', index=False)
    del ngram_freqs4
    EVENT_FILE = "Data/events_4grams.gz"
    df_to_gz(sents_4grams, EVENT_FILE)
    del sents_4grams
    gc.collect()

