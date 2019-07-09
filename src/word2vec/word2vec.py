from os import path
from data_preprocessing import load_dictionary, load_dataset

# constants

BATCH_SIZE = 64             # Number of samples per batch
EMBEDDING_SIZE = 200        # Dimension of the embedding vector
WINDOW_SIZE = 2             # How many words to consider left and right
SAMPLE_SIZE = WINDOW_SIZE * 2 + 1   # Number of tokens in each sample
NEG_SAMPLES = 64            # Number of negative examples to sample
EPOCHS = 100000             # Number of training epochs
TEST_INTERVAL = 500         # Interval between each training test pass
NUM_TRUE = WINDOW_SIZE * 2  # expected words for every input word

DATASET_DIR = r'C:\Users\Sergi\Documents\WIR\dataset'
DATASET_ID = 'ebfe2853a23742d8b6c3f7443f3b4884'
DICTIONARY_PATH = path.join(DATASET_DIR, DATASET_ID + '_words.ls')
DATASET_PATH = path.join(DATASET_DIR, DATASET_ID + '_dataset.ls')
TMP_DIR = "/tmp/"

# dataset loading
dictionary, direct_map, inverse_map = load_dictionary(DICTIONARY_PATH)
print('{} loaded words'.format(len(dictionary)))
dataset = load_dataset(DATASET_PATH, SAMPLE_SIZE)
print('{} loaded sentences'.format(len(dataset)))