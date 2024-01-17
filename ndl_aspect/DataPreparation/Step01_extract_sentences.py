import os
import pandas as pd
from collections import OrderedDict
import numpy as np

WD = os.getcwd()
isExist = os.path.exists('Data')
if not isExist:
    os.mkdir('Data')

# araneum = sys.argv[2]
output = WD + '/Data/extracted_sentences.csv'


def add_length(sent):
    return len(sent.split())


def extract(araneum):
    sents = OrderedDict()
    sent = list()
    tags = list()
    verbs = list()
    lemmas = list()
    pos = list()
    bedzie_tag = str()
    bedzie_verb = str()
    bedzie_pos = int()
    bedzie_lemma = str()
    endofclause = [".", "!", "?", ":", ",", ";", '-']
    with open(araneum) as corpus:
        for i, line in enumerate(corpus):
            # print(line)
            if line.startswith('<'):
                if line.startswith('</s>'):
                    # if len(verbs) < 10:
                    sents[' '.join(sent)] = [verbs, pos, tags, lemmas]
                    tags = list()
                    verbs = list()
                    lemmas = list()
                    pos = list()
                    sent = list()
                    # print(sents[' '.join(sent)])
            else:
                fields = line.split('\t')
                # print(fields)
                if len(fields) >= 4:
                    if fields[0] not in endofclause:
                        sent.append(fields[0])
                    if fields[0] in endofclause or len(sent) - bedzie_pos > 3 or bedzie_pos - len(sent) > 1:
                        bedzie_tag = str()
                        bedzie_lemma = str()
                        bedzie_verb = str()
                        bedzie_pos = int()
                    if fields[2] == 'Vb':
                        # print(verbs)
                        if not fields[3].startswith(('impt', 'imps', 'pcon', 'pant', 'pact', 'ppas', 'ger', 'winien')):
                            if fields[3].split(':')[0] == 'bedzie':
                                if len(pos) > 0:
                                    if isinstance(pos[-1], int):
                                        if len(sent) - pos[-1] <= 2 and ((tags[-1].split(':')[0] == 'inf' and
                                                                          tags[-1].split(':')[-1] == 'imperf') or (
                                                                                 tags[-1].split(':')[0] == 'praet' and
                                                                                 tags[-1].split(':')[-1] == 'imperf')):
                                            verbs[-1] = ' '.join([fields[0], verbs[-1]])
                                            tags[-1] = ' '.join([fields[3], tags[-1]])
                                            lemmas[-1] = ' '.join([fields[1], lemmas[-1]])
                                            pos[-1] = ' '.join([str(pos[-1]), str(len(sent))])
                                else:
                                    bedzie_tag = fields[3]
                                    bedzie_verb = fields[0]
                                    bedzie_pos = len(sent)
                                    bedzie_lemma = fields[1]
                            else:
                                if len(bedzie_tag) != 0 and len(sent) - bedzie_pos <= 4 and (
                                        (fields[3].split(':')[0] == 'inf' and fields[3].split(':')[-1] == 'imperf') or (
                                        fields[3].split(':')[0] == 'praet' and fields[3].split(':')[-1] == 'imperf')):
                                    # print(verbs)
                                    verbs.append(' '.join([bedzie_verb, fields[0]]))
                                    tags.append(' '.join([bedzie_tag, fields[3]]))
                                    lemmas.append(' '.join([bedzie_lemma, fields[1]]))
                                    pos.append(' '.join([str(bedzie_pos), str(len(sent))]))

                                else:
                                    verbs.append(fields[0])
                                    lemmas.append(fields[1])
                                    pos.append(len(sent))
                                    tags.append(fields[3])

    # df = pd.DataFrame({'Sentence': sents, 'Verbs': all_verbs, 'Lemmas': all_lemmas, 'Tags': all_tags})
    print(len(sents))
    # keys = sample(sents.keys(), 1000)
    # sample_d = {k: sents[k] for k in keys}
    # print(len(sample_d))
    sentences_dict = dict()
    for i, (sent, features) in enumerate(sents.items()):
        num_tags = len(features[0])
        if num_tags < 18:
            sentences_dict[i] = dict()
            sentences_dict[i]["Sentence"] = sent
            sentences_dict[i]["num_verbs"] = int(num_tags)
            for j in range(num_tags):
                sentences_dict[i]["verbs_{}".format(j + 1)] = features[0][j]
                sentences_dict[i]["verbs_lemmas_{}".format(j + 1)] = str(features[3][j])
                sentences_dict[i]["verbs_pos_{}".format(j + 1)] = features[1][j]
                sentences_dict[i]["verbs_tags_{}".format(j + 1)] = features[2][j]
    sents = pd.DataFrame.from_dict(sentences_dict, orient="index")

    sents['sentence_length'] = sents.apply(lambda x: add_length(x.loc['Sentence']), axis=1)

    cols = list(sents.columns)
    cols.insert(1, cols.pop(cols.index('sentence_length')))
    sents = sents.loc[:, cols]
    sents['SentenceID'] = np.arange(1, (len(sents) + 1))

    # Move the columns before the 'Sentence' column
    cols = list(sents.columns)
    cols.insert(0, cols.pop(cols.index('SentenceID')))
    sents = sents.loc[:, cols]
    groups = [sents for _, sents in sents.groupby('SentenceID')]
    print(sents.shape)
    with open(output, "w") as res_csv:
        sents.to_csv(res_csv, sep=",", index=False)
