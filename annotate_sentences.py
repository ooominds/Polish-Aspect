def annotate(sents):
    ta_tags = list()
    for i, row in sents.iterrows():
        tags = row['araneum_tags']
        sent = row['Sentence']
        verb = row['verb']
        try:
            bedzie, tags = tags.split(' ')
            tags = tags.split(':')
            if tags[0] == 'inf':
                ta_tags.append('imperf.fut')
            elif tags[0] == 'praet':
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
                        if verb.endswith(('łem', 'łeś', 'ł', 'liśmy', 'liście', 'li', 'łam', 'łaś', 'ła', 'łyśmy', 'łyście', 'ły', 'ło')):
                            ta_tags[-1] = 'imperf.past'
                    else:
                        if verb.endswith(('ła', 'ło')):
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

    sents['TA_Tags'] = ta_tags
    sents = sents[sents.TA_Tags != 'infinitive']
    sents = sents[sents.TA_Tags != 'other']
    sents = sents[sents.TA_Tags != 'aglt']
    print(sents['TA_Tags'].value_counts())
    return sents
