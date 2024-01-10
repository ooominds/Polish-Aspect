import sys
from ndl_aspect.DataPreparation import *
from ndl_aspect.TrainNDL import TrainNDL


dataset_type = sys.argv[1]
araneum = sys.argv[2]
cues_type = sys.argv[3]


### UNCOMMENT THE STEPS YOU ARE INTERESTED IN RUNNING. BE AWARE THAT EACH STEP RELIES ON ALL THE PREVIOUS ONES ####
#Step01_extract_sentences.extract(araneum)
#Step02_annotate_sentences.annotate()
#Step03_find_reflexives.tag_reflexives()
#Step04_prepare_corpus.prepare()
#Step05_extract_lemmas.extract_lemmas()
#Step06_extract_ngrams.extract_ngrams()
#Step07_prepare_cues_to_use.prepare_all_cues()
#Step08_split.splitData(dataset_type)
#Step09_make_eventfiles.make_eventfiles(dataset_type)

TrainNDL.run(dataset_type, cues_type)



