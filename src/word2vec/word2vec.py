import math
import os
import tensorflow as tf
from tensorboard.plugins import projector
from data_preprocessing import load_dictionary, load_dataset, generate_batches
from data_analysis import find_closest
from weights_serialization import save_array, save_vector, load_array, load_vector

# constants

BATCH_SIZE = 128            # number of samples per batch
EMBEDDING_SIZE = 200        # dimension of the embedding vector
WINDOW_SIZE = 2             # how many words to consider left and right
SAMPLE_SIZE = WINDOW_SIZE * 2 + 1   # Number of tokens in each sample
NEG_SAMPLES = 64            # number of negative examples to sample
TRAIN_ITERATIONS = 10000000 # number of training epochs
TEST_INTERVAL = 10000       # interval between each training test pass
NUM_TRUE = WINDOW_SIZE * 2  # expected words for every input word
INTEREST_WORDS = [
    'climate', 'warming',
    'believe', 'science',
    'health', 'denial', 'hoax'
]                           # the words to display at each internal

DATASET_DIR = r'C:\Users\Sergio\Documents\WIR\dataset'
DATASET_ID = '978d3bfaa50a4e028d4c740ba39578df'
DICTIONARY_PATH = os.path.join(DATASET_DIR, DATASET_ID + '_words.ls')
DATASET_PATH = os.path.join(DATASET_DIR, DATASET_ID + '_dataset_1.ls')
TMP_DIR = r'C:\Users\Sergio\Documents\WIR\tmp'

# when resuming training
WEIGHTS_BASE_PATH = r'C:\Users\Sergio\Documents\WIR\tmp\tweets_all_978d3bfaa50a4e028d4c740ba39578df\978d3bfaa50a4e028d4c740ba39578df'
WEIGHTS_PRESENT = WEIGHTS_BASE_PATH != None
WORD_EMBEDDINGS_PATH = WEIGHTS_BASE_PATH + '_word-embeddings.ls'
CONTEXT_EMBEDDINGS_PATH = WEIGHTS_BASE_PATH + '_context-embeddings.ls'
BIASES_PATH = WEIGHTS_BASE_PATH + '_biases.ls'

# dataset loading
dictionary, direct_map, inverse_map = load_dictionary(DICTIONARY_PATH)
DICTIONARY_SIZE = len(dictionary)   # size of the loaded dictionary
print('>> {} loaded words'.format(DICTIONARY_SIZE))
dataset = load_dataset(DATASET_PATH, SAMPLE_SIZE)
print('>> {} loaded sentences'.format(len(dataset)))

# model definition
graph = tf.Graph()
with graph.as_default():

    # input tensors
    with tf.name_scope('inputs'):
        train_inputs = tf.placeholder(tf.int32, shape=[BATCH_SIZE])
        train_labels = tf.placeholder(tf.int32, shape=[BATCH_SIZE, NUM_TRUE]) # outputs for every input word

    # variable tensors
    with tf.name_scope('variables'):
        if not WEIGHTS_PRESENT:
            word_embeddings = tf.Variable(tf.random_uniform([DICTIONARY_SIZE, EMBEDDING_SIZE], -1.0, 1.0), name='word_embeddings')
            context_embeddings = tf.Variable(tf.truncated_normal([DICTIONARY_SIZE, EMBEDDING_SIZE], stddev=1.0 / math.sqrt(EMBEDDING_SIZE)), name='context_embeddings') # swapped shapes for sampled softmax
            output_biases = tf.Variable(tf.zeros([DICTIONARY_SIZE])) # needed by the sampled softmax
        else:
            word_embeddings = tf.Variable(load_array(WORD_EMBEDDINGS_PATH, DICTIONARY_SIZE, EMBEDDING_SIZE), dtype=tf.float32, name='word_embeddings')
            context_embeddings = tf.Variable(load_array(CONTEXT_EMBEDDINGS_PATH, DICTIONARY_SIZE, EMBEDDING_SIZE), dtype=tf.float32, name='context_embeddings')
            output_biases = tf.Variable(load_vector(BIASES_PATH), dtype=tf.float32)
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
print('>> graph created')

# write the metadata for the word embeddings
with open(os.path.join(TMP_DIR, 'metadata.tsv'), 'w', encoding='utf-8') as f:
    for i in range(DICTIONARY_SIZE):
        f.write(inverse_map[i] + '\n')

# training
with tf.Session(graph=graph) as session:

    # initialization
    writer = tf.summary.FileWriter(TMP_DIR, graph)
    init.run() # initialize the variables in the graph
    batches = generate_batches(dataset, WINDOW_SIZE, BATCH_SIZE)
    print('>> session initialized')

    # create the configuration to visualize the embeddings with labels in TensorBoard
    config = projector.ProjectorConfig()
    embedding_conf = config.embeddings.add()
    embedding_conf.tensor_name = word_embeddings.name
    embedding_conf.metadata_path = os.path.join(TMP_DIR, 'metadata.tsv')
    projector.visualize_embeddings(writer, config)
    print('>> added embeddings projector configuration')

    # training loop
    print('============ START ============')
    average_loss = 0
    for i in range(TRAIN_ITERATIONS):

        # get the batch and the metadata
        batch = next(batches)
        run_metadata = tf.RunMetadata()

        # training step
        _, summary, run_loss = session.run(
            [optimizer, merged, loss],
            feed_dict={train_inputs: batch[0], train_labels: batch[1]},
            run_metadata=run_metadata
        )
        average_loss += run_loss

        # write the summary
        writer.add_summary(summary, i)

        # show the progress at each interval
        if i > 0 and i % TEST_INTERVAL == 0:
            print('>> [{}]: loss = {}'.format(i, average_loss / TEST_INTERVAL))
            average_loss = 0

            # display the closest words
            embeddings = session.run(word_embeddings)
            for word in INTEREST_WORDS:
                index = direct_map[word]
                print('    • {}: '.format(word), end='')
                for j in find_closest(index, embeddings, 8):
                    print(inverse_map[j], end=' ')
                print('')

            # save the weights
            save_array(embeddings, os.path.join(TMP_DIR, DATASET_ID + '_word-embeddings.ls'))
            save_array(session.run(context_embeddings), os.path.join(TMP_DIR, DATASET_ID + '_context-embeddings.ls'))
            save_vector(session.run(output_biases), os.path.join(TMP_DIR, DATASET_ID + '_biases.ls'))

            # save the model checkpoint
            saver.save(session, os.path.join(TMP_DIR, 'model.ckpt'))

writer.close()
