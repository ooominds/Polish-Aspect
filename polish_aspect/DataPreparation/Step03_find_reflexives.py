import pandas as pd


def contains_sie(sent, pos, verb, lemmas):
    if ' ' in pos:
        pos = pos.split()[-1]
    if verb in lemmas:
        pos = int(float(pos))
        words = sent.split()
        if len(words) > pos:
            if words[pos] == 'się':
                return 'True'
            else:
                if pos > 2:
                    if words[pos - 2] == 'się':
                        return 'True'
                    else:
                        return 'False'
                else:
                    return 'False'
        else:
            if pos > 2 and len(words) > pos - 2:
                if words[pos - 2] == 'się':
                    return 'True'
                else:
                    return 'False'
            else:
                return 'False'
    else:
        return 'False'


def fix_pos(pos):
    if ' ' in pos:
        return pos.split()[-1]
    else:
        return pos


def fix_infinitive(infinitive):
    if 'BYĆ' in infinitive:
        infinitive = infinitive.replace('BYĆ', '')
        infinitive = infinitive.replace(' ', '')
    if 'BYC' in infinitive:
        infinitive = infinitive.replace('BYC', '')
        infinitive = infinitive.replace(' ', '')
    if 'MIEĆ' in infinitive:
        infinitive = infinitive.replace('MIEĆ', '')
        infinitive = infinitive.replace(' ', '')
    if 'DAĆ' in infinitive:
        infinitive = infinitive.replace('DAĆ', '')
        infinitive = infinitive.replace(' ', '')
    infinitive = infinitive.replace(' ', '#')
    return infinitive


def replace_infinitive(infinitive, sie):
    if sie == 'True':
        return '#'.join([infinitive, 'SIĘ'])
    else:
        return infinitive


def tag_reflexives():
    sample = pd.read_csv('Data/tagged_sentences.gz',
                         usecols=['SentenceID', 'Sentence', 'num_verbs', 'position', 'verb', 'infinitive', 'TA_Tags'])
    lemmas = list()
    with open('DownloadedData/lemmas_sie.txt', 'r') as l:
        lines = l.readlines()
        for line in lines:
            lemmas.append(line.strip().upper())
    sample['infinitive'] = sample.apply(lambda x: x.loc['infinitive'].upper(), axis=1)
    sample['infinitive'] = sample.apply(lambda x: fix_infinitive(x.loc['infinitive']), axis=1)
    sample['pos'] = sample.apply(lambda x: fix_pos(x.loc['pos']), axis=1)
    sample['SIE'] = sample.apply(lambda x: contains_sie(x.loc['Sentence'], x.loc['position'], x.loc['infinitive'], lemmas), axis=1)
    sample['infinitive'] = sample.apply(lambda x: replace_infinitive(x.loc['infinitive'], x.loc['SIE']), axis=1)
    sample.to_csv('Data/tagged_with_sie.gz', index=False)
