import os
import shutil
import pandas as pd

data = pd.read_csv('slice_common_voice.csv')
data['path_wav'] = data.path.apply(lambda x: x.replace('mp3', 'wav'))

slice_files = data.path_wav.tolist()

data_base = '../data/adapted_commonvoice_dataset_wav/'
data_not_suitable = '../data_not_used/'

if not os.path.isdir(data_not_suitable):
    os.mkdir(data_not_suitable)

for file in os.listdir(data_base):
    if file not in slice_files:
        shutil.move(data_base + file, data_not_suitable + file)