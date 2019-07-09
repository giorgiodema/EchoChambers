from os import path
import tensorflow as tf
from data_preprocessing import load_dictionary, load_dataset, generate_batches

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
DICTIONARY_SIZE = len(dictionary)   # size of the loaded dictionary
print('>> {} loaded words'.format(DICTIONARY_SIZE))
dataset = load_dataset(DATASET_PATH, SAMPLE_SIZE)
print('>> {} loaded sentences'.format(len(dataset)))

# model definition
with tf.Graph().as_default():

    # input tensors
    with tf.name_scope('inputs'):
        train_inputs = tf.placeholder(tf.int32, shape=[BATCH_SIZE])
        train_labels = tf.placeholder(tf.int32, shape=[BATCH_SIZE, NUM_TRUE]) # outputs for every input word

    # variable tensors
    with tf_name_scope('variables'):
        word_embeddings = tf.Variable(tf.random_uniform([DICTIONARY_SIZE, EMBEDDING_SIZE], -1.0, 1.0), name='word_embeddings')
        context_embeddings = tf.Variable(tf.truncated_normal([DICTIONARY_SIZE, EMBEDDING_SIZE], stddev=1.0 / math.sqrt(EMBEDDING_SIZE)), name='context_embeddings') # swapped shapes for sampled softmax
        output_biases = tf.Variable(tf.zeros([DICTIONARY_SIZE])) # needed by the sampled softmax
    lookup = tf.nn.embedding_lookup(word_embeddings, train_inputs) # forward inputs to the hidden layer

    # loss
    with tf.name_scope('loss'):
        softmax = tf.nn.sampled_softmax_loss(
            weights=context_embeddings,
            biases=output_biases,
            labels=train_labels,
            inputs=lookup,
            num_classes=DICTIONARY_SIZE,
            num_sampled=NEG_SAMPLES,
            num_true=NUM_TRUE
        )
        loss = tf.reduce_sum(softmax, name='reduce_sum')

    # track the batch loss in the summary
    tf.summary.scalar('loss', loss)

    # optimizer
    with tf.name_scope('optimizer'):
        optimizer = tf.train.AdamOptimizer().minimize(loss)

    # additional objects
    merged = tf.summary.merge_all() # merged summaries
    init = tf.global_variables_initializer() # variables initializer
    saver = tf.train.Saver() # network saver