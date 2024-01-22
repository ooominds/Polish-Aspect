import sys
from ndl_aspect.DataPreparation import *
from ndl_aspect.TrainNDL import TrainNDL
import argparse

parser = argparse.ArgumentParser(description='This script trains an NDL model to predict aspect in Polish verbs.')
parser.add_argument('--stratification', type=str,
                    help='type of sampling stratification')
parser.add_argument('--path_to_local_corpus', type=str,
                    help='Directory path to a local corpus file in the style of Araneum Polonicum')
parser.add_argument('--type_of_cues', type=str,
                    help='type of cues to train NDL')
parser.add_argument('--size_of_sample', type=int, default=0,
                    help='size of sample from Araneum')
parser.add_argument('--num_threads', type=int, default=4,
                    help='number of threads')

args = parser.parse_args()
dataset_type = args.stratification
araneum = args.path_to_local_corpus
cues_type = args.type_of_cues
N = args.size_of_sample
T = args.num_threads


### UNCOMMENT THE STEPS YOU ARE INTERESTED IN RUNNING. BE AWARE THAT EACH STEP RELIES ON ALL THE PREVIOUS ONES ####
#Step01_extract_sentences.extract(araneum)
#Step02_annotate_sentences.annotate()
#Step03_find_reflexives.tag_reflexives()
#Step04_prepare_corpus.prepare(N)
#Step05_extract_lemmas.extract_lemmas()
#Step06_extract_ngrams.extract_ngrams(T)
#Step07_prepare_cues_to_use.prepare_all_cues()
#Step08_split.splitData(dataset_type)
#Step09_make_eventfiles.make_eventfiles(dataset_type)

#TrainNDL.run(dataset_type, cues_type)



