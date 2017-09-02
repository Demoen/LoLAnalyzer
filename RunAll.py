# All script can be called from here

import multiprocessing
import Networks
import Modes

# Running options
cpu = max(multiprocessing.cpu_count() - 1, 1)  # The number of cpu the scripts will use.
shuffling_files = 67  # prime number to maximize spreading. Take a prime higher to the number of data files (e.g. If you have 32 data files, take 37)
keep_for_testing = 1  # Number of files that will be kept for testing only. Increase this number as you get more files (10% is standard)
# Keep in mind testing on games that were not used for training is the only we can be sure the neural network is not recognizing games but has
# actually learned to predict the winner.
restore = False  # leave this to False, or your model will overfit the data (it will recognize the game and not learn why the game is won/loss)

# Mode and Network
# Look at Modes.py and Networks.py to see the list of available modes/networks
# Feel free to build/tune your own networks
# BUT, keep in mind that more complex networks require more data and take more time to train.
mode = Modes.ABR_Mode()
network = Networks.DenseDegressive(mode=mode, n_hidden_layers=2, NN=512, dropout=0.3, batch_size=200, report=10)  # 5327 5244
# mode = Modes.ABR_TJMCS_Mode()
# network = Networks.DenseDegressive(mode=mode, n_hidden_layers=4, NN=1024, dropout=0.0, batch_size=200, report=10)  # 5324 5305 5300

# REMOVE OTJMCS -> use TJMCS for blue and red team

# Scripts to execute, comment useless ones
# In particular, if you just want to run the app, comment all but 'BestPicks'
to_execute = [
    # 'PlayersListing'
    # 'DataDownloader',  # runs on multiple cpu
    # 'DataExtractor',  # runs on multiple cpu
    # 'RoleUpdater',
    'DataProcessing',  # runs on multiple cpu
    'DataShuffling',
    'Learner',  # runs on gpu
    'BestPicks',
]


if __name__ == '__main__':
    if 'PlayersListing' in to_execute:
        import PlayersListing
        PlayersListing.run(mode)
    if 'DataDownloader' in to_execute:
        import DataDownloader
        DataDownloader.run(mode)
    if 'DataExtractor' in to_execute:
        import DataExtractor
        DataExtractor.run(mode, cpu)
    if 'RoleUpdater' in to_execute:
        import RoleUpdater
        RoleUpdater.run(mode)
    if 'DataProcessing' in to_execute:
        import DataProcessing
        DataProcessing.run(mode, cpu)
    if 'DataShuffling' in to_execute:
        import DataShuffling
        DataShuffling.run(mode, shuffling_files, keep_for_testing, cpu)
    if 'Learner' in to_execute:
        import Learner
        Learner.run(mode, network, restore)
    if 'BestPicks' in to_execute:
        import BestPicks
        BestPicks.run(mode, network)
