from pyndl import ndl, activation, preprocess
import pandas as pd
import os
import csv
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
import numpy as np

WD = os.getcwd()
TOP = os.path.abspath(os.path.join(WD, os.pardir)) + '/Polish-Aspect/'


def choose_folder(datatype):
    if datatype == 'balanced':
        folder = 'BalancedData/'
        results = 'BalancedResults/'
        weights = 'BalancedWeights/'
    else:
        folder = 'NDLData/'
        results = 'NDLResults/'
        weights = 'NDLWeights/'
    return folder, results, weights


def choose_cues(cuestype):
    if cuestype == 'all':
        return 'all_cues_to_use.csv', 'ALLCUES/'
    elif cuestype == 'ngrams':
        return 'all_ngrams_to_use.csv', 'ALLNGRAMS/'
    elif cuestype == 'superlemmas':
        return 'all_superlemmas_to_use.csv', 'ALLSUPERLEMMAS/'
    elif cuestype == 'tenses':
        return 'all_tenses_to_use.csv', 'ALLTENSES/'
    elif cuestype == 'ngrams_superlemmas':
        return 'ngrams_superlemmas_to_use.csv', 'NGRAMS_SUPERLEMMAS/'
    elif cuestype == 'superlemmas_tenses':
        return 'superlemmas_tenses_to_use.csv', 'SUPERLEMMAS_TENSES/'
    elif cuestype == 'ngrams_tenses':
        return 'ngrams_tenses_to_use.csv', 'NGRAMS_TENSES/'


class NDLmodel:
    def __init__(self, weights):
        self.weights = weights


def import_index_system(index_system_path, N_tokens=None):
    with open(index_system_path, 'r', encoding='utf-8') as file:
        index_system_df = csv.reader(file)
        index_system_dict = {}
        if N_tokens is None:
            for line in index_system_df:
                k, v = line
                index_system_dict[k] = int(v)
        else:
            for i in range(N_tokens):
                k, v = next(index_system_df)
                index_system_dict[k] = int(v)

    return index_system_dict


def reverse_dictionary(dict_var):
    return {v: k for k, v in dict_var.items()}


def train(events, matrix_folder, cue_index, outcome_index, outcomefolder):
    cues_to_keep = [cue for cue in cue_index.keys()]
    outcomes_to_keep = [outcome for outcome in outcome_index.keys()]
    name = events.rsplit('/', 1)[1]
    filtered_events = preprocess.filter_event_file(events,
                                                   outcomefolder + 'filtered_' + name,
                                                   n_jobs=16,
                                                   keep_cues=cues_to_keep,
                                                   keep_outcomes=outcomes_to_keep)
    weights = ndl.ndl(events=outcomefolder + 'filtered_' + name,
                      alpha=0.01, betas=(1, 1),
                      number_of_threads=16,
                      method='threading',
                      remove_duplicates=True)
    # stores learned weights in NetCDF format
    matrix = matrix_folder + name.replace('gz', 'nc')
    weights.to_netcdf(matrix)
    return weights


def activations_to_predictions(activations):
    # Predicted tenses from the activations
    y_pred = []
    for j in range(activations.shape[1]):
        activation_col = activations[:, j]
        try:  # If there is a single max
            argmax_j = activation_col.where(activation_col == activation_col.max(), drop=True).squeeze().coords[
                'outcomes'].values.item()
        except:  # If there are multiple maxes
            maxes = activation_col.where(activation_col == activation_col.max(), drop=True).values
            argmax_j = np.random.choice(maxes, 1, replace=False).squeeze()
        y_pred.append(argmax_j)
    return y_pred


def predict(test_events, test_set, matrix, outcome_to_index, results_folder, no_processes, cue_to_index):
    test_weights = activation.activation(test_events, matrix, number_of_threads=no_processes, remove_duplicates=False,
                                         ignore_missing_cues=True)
    events = pd.read_csv(test_events, sep='\t', na_filter=False, encoding='utf-8')
    test_set = pd.read_csv(test_set, sep=',', na_filter=False, encoding='utf8')
    y_test = events['outcomes'].tolist()
    y_pred = activations_to_predictions(test_weights)
    test_accuracy = accuracy_score(y_test, y_pred)
    print('Accuracy :', test_accuracy)
    index_to_outcome = reverse_dictionary(outcome_to_index)
    cmat = confusion_matrix(y_test, y_pred, labels=list(outcome_to_index.keys()))  # Confusion matrix
    pmat = cmat.diagonal() / cmat.sum(axis=1)  # Confusion matrix in terms of proportions
    print({index_to_outcome[j + 1]: round(pmat[j], 4) for j in range(len(pmat))})
    f1 = f1_score(y_test, y_pred, average=None, labels=list(outcome_to_index.keys()))
    print({index_to_outcome[j + 1]: round(f1[j], 2) for j in range(len(f1))})
    results_test = test_set[
        ['SentenceID', 'Sentence', 'verb', 'position', 'Aspect', 'Cues']].copy()
    results_test['Predicted'] = y_pred
    allowed_cues = set(cue_to_index.keys())
    results_test['FilteredCues'] = results_test['Cues'].apply(
        lambda s: '_'.join([cue for cue in s.split('_') if cue in allowed_cues]))
    results_test.drop(columns=['Cues'], inplace=True)
    results_test['Accuracy'] = results_test.apply(lambda x: int(x.loc['Aspect'] == x.loc['Predicted']), axis=1)
    results_test = results_test.loc[:,
                   ['SentenceID', 'Sentence', 'verb', 'position', 'Aspect', 'FilteredCues', 'Predicted', 'Accuracy']]
    name = test_events.rsplit('/', 1)[1]
    results_test.to_csv(results_folder + name.replace('gz', 'csv'), sep=',', index=False)


def run(dataset_type, cues_type):
    folder, result_folder, weights_folder = choose_folder(dataset_type)
    cuetype, subfolder = choose_cues(cues_type)
    cue_index_file = TOP + 'Data/' + cuetype
    outcome_index_file = TOP + 'ndl_aspect/DataPreparation/DownloadedData/outcome_index.csv'
    train_events = TOP + folder + 'events_train_set.gz'
    test_events = TOP + folder + 'events_test_set.gz'
    test_file = TOP + folder + 'test_set.gz'
    cue_to_index = import_index_system(cue_index_file)
    outcome_index = import_index_system(outcome_index_file)
    isExist = os.path.exists(weights_folder)
    if not isExist:
        os.mkdir(weights_folder)
    isExist = os.path.exists(weights_folder + subfolder)
    if not isExist:
        os.mkdir(weights_folder + subfolder)
    isExist = os.path.exists(result_folder)
    if not isExist:
        os.mkdir(result_folder)
    isExist = os.path.exists(result_folder + subfolder)
    if not isExist:
        os.mkdir(result_folder + subfolder)
    isExist = os.path.exists(folder+subfolder)
    if not isExist:
        os.mkdir(folder+subfolder)
    weights = train(train_events, weights_folder + subfolder, cue_to_index, outcome_index, folder + subfolder)
    predict(test_events, test_file, weights, outcome_index, result_folder + subfolder, 16, cue_to_index)



