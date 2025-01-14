from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import json
import math
import os
import modeling
import optimization
import tokenization
import six
import tensorflow as tf

flags = tf.flags

FLAGS = flags.FLAGS

MODEL_DIR = '../data/bert_base_uncased/'
QuAC_DIR = '../data/QuAC/'

CHKPT_PATH = 'outputs/model_18000.ckpt'

# for running in jupyter env
flags.DEFINE_string('f', '', 'kernel')

## Required parameters
flags.DEFINE_string(
    "bert_config_file", MODEL_DIR+"bert_config.json",
    "The config json file corresponding to the pre-trained BERT model. "
    "This specifies the model architecture.")

flags.DEFINE_string("vocab_file", MODEL_DIR+"vocab.txt",
                    "The vocabulary file that the BERT model was trained on.")

flags.DEFINE_string(
    "output_dir", "outputs/",
    "The output directory where the model checkpoints will be written.")

flags.DEFINE_string("quac_train_file", QuAC_DIR+"train_v0.2.json",
                    "QuAC json for training.")

flags.DEFINE_string(
    "quac_predict_file", QuAC_DIR+"val_v0.2.json",
    "QuAC json for predictions.")

# flags.DEFINE_string(
#     "init_checkpoint", MODEL_DIR+"bert_model.ckpt",
#     "Initial checkpoint (usually from a pre-trained BERT model).")

flags.DEFINE_string(
    "init_checkpoint", CHKPT_PATH,
    "Initial checkpoint (usually from a pre-trained BERT model).")


flags.DEFINE_bool(
    "do_lower_case", True,
    "Whether to lower case the input text. Should be True for uncased "
    "models and False for cased models.")

flags.DEFINE_integer(
    "max_seq_length", 512,
    "The maximum total input sequence length after WordPiece tokenization. "
    "Sequences longer than this will be truncated, and sequences shorter "
    "than this will be padded.")

flags.DEFINE_integer(
    "doc_stride", 128,
    "When splitting up a long document into chunks, how much stride to "
    "take between chunks.")

flags.DEFINE_integer(
    "max_query_length", 64,
    "The maximum number of tokens for the question. Questions longer than "
    "this will be truncated to this length.")

flags.DEFINE_bool("do_train", True, "Whether to run training.")

flags.DEFINE_bool("do_predict", True, "Whether to run eval on the dev set.")

flags.DEFINE_integer("train_batch_size", 4, "Total batch size for training.")

flags.DEFINE_integer("predict_batch_size", 4,
                     "Total batch size for predictions.")

flags.DEFINE_float("learning_rate", 3e-5, "The initial learning rate for Adam.")

flags.DEFINE_float("num_train_epochs", 2.0,
                   "Total number of training epochs to perform.")

flags.DEFINE_float(
    "warmup_proportion", 0.1,
    "Proportion of training to perform linear learning rate warmup for. "
    "E.g., 0.1 = 10% of training.")

flags.DEFINE_integer("save_checkpoints_steps", 10000,
                     "How often to save the model checkpoint.")

flags.DEFINE_integer("evaluation_steps", 5000,
                     "How often to do evaluation.")

flags.DEFINE_integer("evaluate_after", 0,
                     "we do evaluation after centain steps.")

flags.DEFINE_integer("iterations_per_loop", 1000,
                     "How many steps to make in each estimator call.")

flags.DEFINE_integer(
    "n_best_size", 4,
    "The total number of n-best predictions to generate in the "
    "nbest_predictions.json output file.")

flags.DEFINE_integer(
    "max_answer_length", 30,
    "The maximum length of an answer that can be generated. This is needed "
    "because the start and end predictions are not conditioned on one another.")

flags.DEFINE_bool("use_tpu", False, "Whether to use TPU or GPU/CPU.")

tf.flags.DEFINE_string(
    "tpu_name", None,
    "The Cloud TPU to use for training. This should be either the name "
    "used when creating the Cloud TPU, or a grpc://ip.address.of.tpu:8470 "
    "url.")

tf.flags.DEFINE_string(
    "tpu_zone", None,
    "[Optional] GCE zone where the Cloud TPU is located in. If not "
    "specified, we will attempt to automatically detect the GCE project from "
    "metadata.")

tf.flags.DEFINE_string(
    "gcp_project", None,
    "[Optional] Project name for the Cloud TPU-enabled project. If not "
    "specified, we will attempt to automatically detect the GCE project from "
    "metadata.")

tf.flags.DEFINE_string("master", None, "[Optional] TensorFlow master URL.")

flags.DEFINE_integer(
    "num_tpu_cores", 8,
    "Only used if `use_tpu` is True. Total number of TPU cores to use.")

flags.DEFINE_bool(
    "verbose_logging", False,
    "If true, all of the warnings related to data processing will be printed. "
    "A number of warnings are expected for a normal SQuAD evaluation.")

flags.DEFINE_integer(
    "history", 5,
    "Number of conversation history to use. "
)


flags.DEFINE_bool(
    "only_history_answer", True,
    "only prepend history answers without questions?")

flags.DEFINE_bool(
    "use_history_answer_marker", True,
    "use markers for hisotory answers instead of prepending them."
    "This referes to HAE in our implementation. This flag surpasses the only_history_answer flag.")

flags.DEFINE_bool(
    "load_small_portion",False,
    "during develping, we only want to load a very small portion of "
    "the data to see if the code works.")


flags.DEFINE_string("dataset", 'quac', 'dataset name')

flags.DEFINE_string(
    "cache_dir", "cache/",
    "we store generated features here, so that we do not need to generate them every time")

flags.DEFINE_integer(
    "max_considered_history_turns", 11,
    "we only consider k history turns that immediately precede the current turn when generating the features,"
    "training will be slow if this is set to a large number")


flags.DEFINE_integer(
    "train_steps", 24000,
    "how many train steps")

