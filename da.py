import numpy as np
import tensorflow.compat.v1 as tf
import tensorflow_hub as hub
import tensorflow_text as tf_text
tf.disable_eager_execution()

n_layer = 12
d_model = 768
max_gen_len = 128

def generate(module, inputs, mems):
  """Generate text."""
  inputs = tf.dtypes.cast(inputs, tf.int64)
  generation_input_dict = dict(input_tokens=inputs)
  mems_dict = {}
  for i in range(n_layer):
    mems_dict["mem_{}".format(i)] = mems[i]
  generation_input_dict.update(mems_dict)

  generation_outputs = module(generation_input_dict, signature="prediction",
                              as_dict=True)
  probs = generation_outputs["probs"]

  new_mems = []
  for i in range(n_layer):
    new_mems.append(generation_outputs["new_mem_{}".format(i)])

  return probs, new_mems

g = tf.Graph()
with g.as_default():
  module = hub.Module("https://tfhub.dev/google/wiki40b-lm-th/1")
  text = ["\n_START_ARTICLE_\nการนัดหยุดเรียนเพื่อภูมิอากาศ\n_START_SECTION_\nเกรียตา ทืนแบร์ย\n_START_PARAGRAPH_\nวันที่ 20 สิงหาคม 2561 เกรียตา ทืนแบร์ย นักกิจกรรมภูมิอากาศชาวสวีเดน ซึ่งขณะนั้นศึกษาอยู่ในชั้นเกรด 9 (เทียบเท่ามัธยมศึกษาปีที่ 3) ตัดสินใจไม่เข้าเรียนจนกระทั่งการเลือกตั้งทั่วไปในประเทศสวีเดนปี"]

  # Word embeddings.
  embeddings = module(dict(text=text), signature="word_embeddings",
                      as_dict=True)
  embeddings = embeddings["word_embeddings"]

  # Activations at each layer.
  activations = module(dict(text=text),signature="activations", as_dict=True)
  activations = activations["activations"]

  # Negative log likelihood of the text, and perplexity.
  neg_log_likelihood = module(dict(text=text), signature="neg_log_likelihood",
                              as_dict=True)
  neg_log_likelihood = neg_log_likelihood["neg_log_likelihood"]
  ppl = tf.exp(tf.reduce_mean(neg_log_likelihood, axis=1))

  # Tokenization and detokenization with the sentencepiece model.
  token_ids = module(dict(text=text), signature="tokenization", as_dict=True)
  token_ids = token_ids["token_ids"]

  detoken_text = module(dict(token_ids=token_ids), signature="detokenization",
                        as_dict=True)
  detoken_text = detoken_text["text"]

  # Generation
  mems_np = [np.zeros([1, 0, d_model], dtype=np.float32) for _ in range(n_layer)]
  inputs_np = token_ids
  sampled_ids = []
  for step in range(max_gen_len):
    probs, mems_np = generate(module, inputs_np, mems_np)
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

# Initialize session.
with tf.Session(graph=g) as session:
  session.run(init_op)
  embeddings, neg_log_likelihood, ppl, activations, token_ids, detoken_text, generated_text = session.run([
    embeddings, neg_log_likelihood, ppl, activations, token_ids, detoken_text, generated_text])
print(embeddings)
print(neg_log_likelihood)
print(ppl)
print(activations)
print(token_ids)
print(detoken_text)
print(generated_text)
