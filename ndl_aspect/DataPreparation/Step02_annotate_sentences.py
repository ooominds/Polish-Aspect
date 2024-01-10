import pandas as pd
import os
import numpy as np
import csv

WD = os.getcwd()


sents_prepared = WD + '/Data/prepared_sents.gz'
sents_one_per_verb = WD + '/Data/one_per_verb_sents.csv'
output = WD + '/Data/tagged_sentences.gz'


######################################
# Remove sentences with no articles
######################################
def annotate():
    sents = pd.read_csv(WD + '/Data/extracted_sentences.csv')
    sents = sents[sents.num_verbs != 0]

    # Export the dataset
    sents.to_csv(sents_prepared, index=False)

    #####################################
    # New dataset with one article per row
    #####################################

    sents = pd.read_csv(sents_prepared)
    nC = sents.shape[1]  # number of columns
    nR = sents.shape[0]  # number of rows
    nA = int((nC - 5) / 4)  # number of verbs
    with open(sents_one_per_verb, mode='w') as file:
        csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        heading = list(sents.columns[0:4])
        heading.extend(['verb', 'infinitive', 'araneum_tags', 'position'])
        csv_writer.writerow(heading)
        for i in range(0, nR):
            for j in range(1, (nA + 1)):
                if str(sents.at[i, "".join(['verbs_', str(j)])]) != 'nan':
                    colnames_touse = ['SentenceID', 'Sentence', 'sentence_length', 'num_verbs']
                    colnames_touse.extend([colname + str(j) for colname in ['verbs_']])
                    colnames_touse.extend([colname + str(j) for colname in ['verbs_lemmas_']])
                    colnames_touse.extend([colname + str(j) for colname in ['verbs_tags_']])
                    colnames_touse.extend(['verbs_pos_' + str(j)])
                    # _ = csv_writer.writerow(list(articles.iloc[i][colnames_touse]))
                    _ = csv_writer.writerow(list(sents.iloc[i][colnames_touse]))
                    file.flush()
                else:
                    break

    sents = pd.read_csv(sents_one_per_verb)
    # sents.rename(columns={'lemma':'pos', 'tags':'infinitive', 'position':'araneum_tags'}, inplace=True)

    ta_tags = list()
    tags_dict = dict()
    for i, row in sents.iterrows():
        # print(i)
        tags = row['araneum_tags']
        sent = row['Sentence']
        verb = row['verb']
        # tags = row['tags'].split(':')
        try:
            bedzie, tags = tags.split(' ')
            tags = tags.split(':')
            if tags[0] == 'inf' or tags[0] == 'praet':
                ta_tags.append('imperf.fut')
            else:
                ta_tags.append('other')
        except ValueError:
            if tags == 'fin:pl:pri:imperf' and row['verb'].endswith(('liśmy', 'łyśmy')):
                ta_tags.append('imperf.past')
            else:
                tags = tags.split(':')
                if tags[0] == 'fin':
                    if tags[-1] == 'imperf':
                        ta_tags.append('imperf.pres')
                        if verb.endswith(('łem', 'łeś', 'ł', 'liśmy', 'liście', 'li', 'łam', 'łaś', 'ła', 'łyśmy',
                                          'łyście', 'ły', 'ło')):
                            ta_tags[-1] = 'imperf.past'
                    else:
                        if verb.endswith(('łem', 'łeś', 'ł', 'liśmy', 'liście', 'li', 'łam', 'łaś', 'ła', 'łyśmy',
                                          'łyście', 'ły', 'ło')):
                            ta_tags.append('perf.past')
                        else:
                            ta_tags.append('perf.fut')
                elif tags[0] == 'inf':
                    ta_tags.append('infinitive')
                elif tags[0] == 'praet':
                    if not verb.endswith(('by', 'bym', 'byś', 'byśmy', 'byście')) and all(
                            word in sent for word in ['żeby', 'żebym', 'żebyś', 'żebyśmy', 'żebyście', 'by']) == False:
                        if tags[-1] == 'imperf':
                            ta_tags.append('imperf.past')
                        else:
                            ta_tags.append('perf.past')
                    else:
                        ta_tags.append('other')
                else:
                    ta_tags.append('aglt')
        # sentid = row['SentenceID']
        # tags_dict[sentid] = ta_tags[i]

    # print(tags_dict.keys())
    sents['TA_Tags'] = ta_tags
    sents = sents[sents.TA_Tags != 'infinitive']
    sents = sents[sents.TA_Tags != 'other']
    sents = sents[sents.TA_Tags != 'aglt']
    sents = sents[sents.infinitive != 'być']
    sents = sents[sents.infinitive != 'móc']
    sents = sents[sents.infinitive != 'biec']
    sents = sents[sents.infinitive != 'pomóc']
    sents = sents[sents.infinitive != 'piec']
    # sents = sents[sents.TA_Tags.apply(lambda x: len(x)<3)]
    print(sents['TA_Tags'].value_counts())
    sents.to_csv(output, encoding='utf-8', index=False)
