# moving consecutive lines from the same file in different files
# it's not a real shuffle but it spreads the data as much as possible


import pandas as pd
import os

import sys

import Modes


def shuffling(mode, dataFile, nb_files):
    df = pd.read_csv(os.path.join(mode.PREPROCESSED_DIR, dataFile), header=None)
    for i in range(nb_files):
        currentFile = os.path.join(mode.SHUFFLED_DIR, 'data_' + str(i+1) + '.csv')
        print(currentFile)
        index = [k * nb_files + i for k in range(len(df)//nb_files) if k * nb_files + i < len(df)]
        data = df.iloc[index, :]
        data.to_csv(currentFile, mode='a', header=False, index=False)
    print(dataFile, 'DONE')


def validationInput(msg, validAns):
    while True:
        data = input(msg)
        if data.lower() in validAns:
            return data
        print('Incorrect value. Only', validAns, 'are accepted')


def run(mode, nb_files, reshuffle=True):
    assert type(mode) in [Modes.ABOTJMCS_Mode, Modes.ABOT_Mode, Modes.BR_Mode], 'Unrecognized mode {}'.format(mode)
    if os.path.isdir(mode.SHUFFLED_DIR):
        print('WARNING PREVIOUS SHUFFLED DATA FOUND', file=sys.stderr)
        if not reshuffle or validationInput('Do you want to reshuffle the data anyway (take a while)? (y/n)', ['y', 'n']) == 'n':
            return

        import shutil
        if not os.access(mode.SHUFFLED_DIR, os.W_OK):
            # Is the error an access error ?
            os.chmod(mode.SHUFFLED_DIR, os.stat.S_IWUSR)
        shutil.rmtree(mode.SHUFFLED_DIR)
    os.makedirs(mode.SHUFFLED_DIR)

    # listing extracted files and sorting
    preprocessed_files = [f for f in os.listdir(mode.PREPROCESSED_DIR)]
    l = list(map(lambda x: int(x.replace('data_', '').replace('.csv', '')), preprocessed_files))
    l = sorted(range(len(l)), key=lambda k: l[k])
    preprocessed_files = [preprocessed_files[k] for k in l]
    for file in preprocessed_files:
        shuffling(mode, file, nb_files)

if __name__ == '__main__':
    run(Modes.BR_Mode())
