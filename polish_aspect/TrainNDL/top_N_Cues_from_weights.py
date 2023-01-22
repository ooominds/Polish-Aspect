import pandas as pd
import xarray as xr
import os

TOP = '/rds/projects/d/divjakd-ooo-machines/Users/irene/Polish_Paper_New/'
WD = TOP + 'Train/'
os.chdir(WD)
LOCATION_OF_WEIGHTS = WD + 'NewWeights/weights_ngrams_lemmas_tenses.nc'

# Where to save the weights opened and converted to a csv format
#SAVE_WEIGHTS_CSV = "work/OoOM/Marta/weights_skipgrams_no_lemmas.csv"

#  Path to where the results are saved
TOP_10_CUES = WD + 'NewAnalysis/top_100_cues_ngrams_lemmas_tense.csv'
TOP_10_CUES_NO_LEMMAS = WD + 'NewAnalysis/top_100_cues_ngrams_no_lemmas_tensee.csv'
LIST_OF_LEMMAS = TOP + 'PrepareData/FinalData/superlemmas.csv'
# How many rows to saves
N = 100


lemmas_df = pd.read_csv(LIST_OF_LEMMAS, names=['lemmas'])
lemmas_df.rename(columns={'lemmas':'cues'}, inplace=True)
lemmas = lemmas_df.cues.to_list()
ds = xr.open_dataset(LOCATION_OF_WEIGHTS)
print(ds.head())
#ds.to_dataframe().to_csv('Weights/weights.csv')
weights = pd.DataFrame(ds.variables['__xarray_dataarray_variable__'].values).T
weights.columns = ds.variables['outcomes']
weights['cues'] = ds.variables['cues']
ta_tags = ['imperf', 'perf']
frame_list = list()
for tag in ta_tags:
    top = weights.sort_values(tag, ascending=False)[['cues', tag]]
    top.rename(columns={'cues': tag}, inplace=True)
    top.reset_index(drop=True, inplace=True)
    frame_list.append(top)
new_frame = pd.concat(frame_list, axis=1)
#print(new_frame.head(N))
new_frame.head(N).to_csv(TOP_10_CUES, index=False)


frame_list2 = list()
for tag in ta_tags:
    top = weights.sort_values(tag, ascending=False)[['cues', tag]]
    top['cues'] = top['cues'].apply(lambda s: '_'.join([cue for cue in s.split('_') if cue not in lemmas]))
    top = top[~top['cues'].isin(lemmas)]
    common = top.merge(lemmas_df, on=['cues'])
    top = top[~top.cues.isin(common.cues)]
    top.rename(columns={'cues': tag}, inplace=True)
    top.reset_index(drop=True, inplace=True)
    frame_list2.append(top)
new_frame2 = pd.concat(frame_list2, axis=1)
print(new_frame.head(N))
new_frame2.head(N).to_csv(TOP_10_CUES_NO_LEMMAS, index=False)