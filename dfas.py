import tensorflow.compat.v1 as tf
import tensorflow_hub as hub
import tensorflow_text as tf_text
tf.disable_eager_execution()

module_url = "https://tfhub.dev/google/wiki40b-lm-th/1"
embed = hub.Module(module_url, trainable=True)
text = ['ทดสอบ']
embeddings = embed(dict(text=text), signature="word_embeddings",
                      as_dict=True)
embeddings = embeddings["word_embeddings"]
print(embeddings.shape)  # (3,128)
print(embeddings)

# This is a path to an uncased (all lowercase) version of BERT
BERT_MODEL_HUB = "https://tfhub.dev/google/wiki40b-lm-th/1"
n_layer = 12
d_model = 768
max_gen_len = 128

g = tf.Graph()
with g.as_default():
    module_url = "https://tfhub.dev/google/wiki40b-lm-th/1"
    embed = hub.Module(module_url)
    text = ['ทดสอบ']
    embeddings = embed(dict(text=text), signature="word_embeddings",
                       as_dict=True)
    embeddings = embeddings["word_embeddings"]

    init_op = tf.group([tf.global_variables_initializer(),
                        tf.tables_initializer()])

with tf.Session(graph=g) as session:
  session.run(init_op)
  embeddings = session.run([embeddings])
print(embeddings)