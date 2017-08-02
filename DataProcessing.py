import configparser
from collections import OrderedDict

import numpy as np
import multiprocessing
import pandas as pd
import os

SAVE = 1000
CHAMPIONS_SIZE = 150
PATCHES_SIZE = 149
INPUT_SIZE = CHAMPIONS_SIZE * 8 + PATCHES_SIZE + 1 + 1  # team color + team win
config = configparser.ConfigParser()
config.read('config.ini')
DATABASE = config['PARAMS']['database']
EXTRACTED_DIR = os.path.join(DATABASE, 'extracted')
PREPROCESSED_DIR = os.path.join(DATABASE, 'data')
PATCHES = config['PARAMS']['patches'].replace('.', '_').split(',')
PATCHES.extend((PATCHES_SIZE - len(PATCHES)) * [None])
CHAMPIONS_LABEL = config['PARAMS']['sortedChamps'].split(',')
CHAMPIONS_STATUS = ['A', 'B', 'O', 'T', 'J', 'M', 'C', 'S']
np.set_printoptions(formatter={'float_kind': lambda x: "%.2f" % x}, linewidth=200)


if not os.path.isdir(PREPROCESSED_DIR):
    os.makedirs(PREPROCESSED_DIR)

names = CHAMPIONS_LABEL[:]
names.append('patch')
names.append('team')
names.append('win')
names.append('file')
dtype = {champ: str for champ in CHAMPIONS_LABEL}
dtype['patch'] = str
dtype['team'] = int
dtype['win'] = int
dtype['file'] = str


def processing(dataFile):
    currentFile = os.path.join(PREPROCESSED_DIR, dataFile)
    if os.path.isfile(currentFile):
        try:
            preprocessed_df = pd.read_csv(currentFile, header=None)
        except:
            preprocessed_df = []
    else:
        preprocessed_df = []
    df = pd.read_csv(os.path.join(EXTRACTED_DIR, dataFile), names=names, dtype=dtype, skiprows=1)
    print(currentFile, len(df) - len(preprocessed_df), "rows to analyze")
    data = pd.DataFrame(columns=range(INPUT_SIZE))
    for i in range(len(preprocessed_df), len(df)):
        if i % SAVE == 0 and i != len(preprocessed_df):  # saving periodically because the process is rather long
            print(currentFile, len(df)-i)
            data = data.astype(int)
            data.to_csv(currentFile, mode='a', header=False, index=False)
            data = pd.DataFrame(columns=range(INPUT_SIZE))

        # data: win + champions status + patch
        row = df.iloc[i]
        row_data = list()
        row_data.extend([1 if row[CHAMPIONS_LABEL[k]] == s else 0 for k in range(len(CHAMPIONS_LABEL)) for s in CHAMPIONS_STATUS])
        row_data.extend([0 for k in range(CHAMPIONS_SIZE - len(CHAMPIONS_LABEL)) for s in CHAMPIONS_STATUS ])
        row_data.extend([1 if row['patch'] == PATCHES[k] else 0 for k in range(PATCHES_SIZE)])
        row_data.append(row['team'])
        row_data.append(row['win'])
        data.loc[len(data)] = row_data
    if len(data):
        data = data.astype(int)
        data.to_csv(currentFile, mode='a', header=False, index=False)
    print(currentFile, 'DONE')


def processData(netType):
    if netType == 'Value':
        # listing extracted files and sorting
        extracted_files = [f for f in os.listdir(EXTRACTED_DIR)]
        l = list(map(lambda x: int(x.replace('data_', '').replace('.csv', '')), extracted_files))
        l = sorted(range(len(l)), key=lambda k:l[k])
        extracted_files = [extracted_files[k] for k in l]

        cpu = multiprocessing.cpu_count() - 1
        pool = multiprocessing.Pool(processes=cpu)
        pool.map(processing, extracted_files)
    else:
        raise Exception('unknown netType', netType)


if __name__ == '__main__':
    netType = 'Value'
    processData(netType)
