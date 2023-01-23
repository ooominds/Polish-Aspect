# Polish-Aspect

A package for training an NDL model to learn aspect in Polish verbs using pyndl; it can also be used to convert NKJP tags in Tense and Aspect tags. 

## installation

This should be installable from PyPi so this means it requires pip. 
You can install the latest pip by typing "pip install pip".
From a terminal, type "pip install ndl-polish-aspect".

## pipeline

The pipeline.py file (found in the GitHub repository) acts as a step-by-step guide to run the code from data preparation and annotation, to model simulations, to data postprocessing and plotting.
The script requires three input arguments: the type of stratification of the data (specify 'balanced' for balanced dataset, else 'stratified' for frequency sampling); the path to the downloaded Araneum Polonicum, and the cues you want to include, choose from:
- 'all'
- 'superlemmas'
- 'tenses'
- 'ngrams_superlemmas'
- 'superlemmas_tenses'
- 'ngrams_tenses'

### Data Preparation
#### Step I: Create sentences file from corpus file with verb tags 
 - Main File: Step01_extract_sentences.py - requires the path to the corpus (not provided with the package due to licensing)

#### Step II: Convert verb tags into tenses and aspects (tense aspect annotation) 

- Main file: Step02_annotate_sentences.py.  
NOTE: This script contains a set of heuristics for tagging verbs with tense and aspect; these rules exploited the tags extracted from Araneum, which follow the National Corpus of Polish (NKJP) labelling conventions, as well as lexical cues in the sentence, such as the presence of ‘być’ or whether the verb had certain endings. The script only considers indicative mood and discards any sentences in the corpus which are in the indicative.


#### Step III: Find reflexives
- Main file: Step03_find_reflexives.py  
NOTE: The original lemma provided by Araneum did not take reflexive forms into account; this script contains a set of heuristics to correctly label reflexives.

#### Step IV: Prepare corpus
- Main file: Step04_prepare_corpus.py - This script extracts ngrams and assigns a superlemma to each verb based on the dictionary file aspectual_pairs.pickle provided in DataPreparation/DownloadedData; moreover, it removes sentences for which a superlemma is not provided and extracts a sample of 10,000, stratified on Tense Aspect tags.

#### Step V: Extract superlemmas
- Main file: Step05_extract_lemmas.py

#### Step VI: Extract ngrams
- Main file: Step06_extract_ngrams.py

#### Step VII: Prepare cues
- Main file: Step07_prepare_cues_to_use.py - This script produces various files containing the cues needed to filter the event files at a later stage based on input argument 3.

#### Step VIII: Split dataset
- Main file: Step08_split.py - this splits our corpus in training and testing files

#### Step IX: Make eventfiles
- Main file: Step09_make_eventfiles.py - this produces training and test files in the format required by NDL, cues and outcomes in tab separated columns for each learning event


### NDL

#### Train model
- Main file: TrainNDL.py - this script runs an NDL simulation on the chosen dataset (argument 1), using the cues of interest (argument 3), and produces a results file containing predicted aspect for each test sentence, and a weight file representing the association matrix of cues and outcomes.


## contributors

This packages is based on code written for R by Adnane Ez-zizi - date of last change 06/08/2020. This code was corrected, updated and adapted as a Python package by Irene Testini, completed January 2023.

The tense-aspect annotation heuristics were provided by Dagmar Divjak.

Work by all contributors was funded by Leverhulme Trust Leadership Award RL-2016-001 to Dagmar Divjak.
