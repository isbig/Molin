# -*- coding: utf-8 -*-
import numpy as np
import tensorflow.compat.v1 as tf
import tensorflow_hub as hub
import tensorflow_text as tf_text
tf.disable_eager_execution()

# This is a path to an uncased (all lowercase) version of BERT
BERT_MODEL_HUB = "https://tfhub.dev/google/wiki40b-lm-th/1"
n_layer = 12
d_model = 768
max_gen_len = 128

g = tf.Graph()
with g.as_default():
    module_url = "https://tfhub.dev/google/wiki40b-lm-th/1"
    module = hub.Module(module_url)
    text = [u'ทำอะไร']
    # Tokenization and detokenization with the sentencepiece model.
    token_ids = module(dict(text=text), signature="tokenization", as_dict=True)
    token_ids = token_ids["token_ids"]

    inputs_np = token_ids
    inputs = tf.dtypes.cast(inputs_np, tf.int64)

    mems = [np.zeros([1, 0, d_model], dtype=np.float32) for _ in range(n_layer)]

    generation_input_dict = dict(input_tokens=inputs)

    mems_dict = {}
    for i in range(n_layer):
        mems_dict["mem_{}".format(i)] = mems[i]
    generation_input_dict.update(mems_dict)

    generation_outputs = module(generation_input_dict, signature="prediction",
                                as_dict=True)

    probs = generation_outputs["probs"]

    new_mems = []
    sampled_ids = []
    for i in range(n_layer):
        new_mems.append(generation_outputs["new_mem_{}".format(i)])

        sampled_id = tf.random.categorical(tf.math.log(probs[0]), num_samples=1, dtype=tf.int32)
        sampled_id = tf.squeeze(sampled_id)
        sampled_ids.append(sampled_id)
        inputs_np = tf.reshape(sampled_id, [1, 1])

    sampled_ids = tf.expand_dims(sampled_ids, axis=0)
    generated_text = module(dict(token_ids=sampled_ids),
                            signature="detokenization", as_dict=True)
    generated_text = generated_text["text"]

    init_op = tf.group([tf.global_variables_initializer(),
                        tf.tables_initializer()])

with tf.Session(graph=g) as session:
  session.run(init_op)
  token_ids, generation_outputs, generated_text = session.run([token_ids, generation_outputs, generated_text])
print(token_ids)
print(generation_outputs)
print(generated_text)
for a in generated_text:
    print(a.decode('utf8'))