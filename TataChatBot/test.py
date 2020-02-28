import tensorflow as tf
graph = tf.Graph()
with graph.as_default():
    train_inputs = tf.placeholder(tf.int32, shape=[batch_size])
    train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])
    embeddings = tf.Variable(tf.random_uniform([vocabulary_size, embedding_size],   -1.0, 1.0))
    embed = tf.nn.embedding_lookup(embeddings, train_inputs)
    nce_weights = tf.Variable(tf.truncated_normal([vocabulary_size, embedding_size],  stddev=  1.0 / math.sqrt(embedding_size)))
    nce_biases = tf.Variable(tf.zeros([vocabulary_size]))
    loss = tf.reduce_mean( tf.nn.nce_loss(weights=nce_weights, biases=nce_biases, labels=train_labels, inputs=embed, num_sampled=num_sampled, num_classes=vocabulary_size))
    optimizer = tf.train.GradientDescentOptimizer(1.0).minimize(loss)
    init = tf.global_variables_initializer()

#######################################################################################33
# import json
# new_selected_list =[]
#
# def data_clean():
#     with open("test.json", 'r') as f:
#         datastore = json.load(f)
#     #
#     datarestore=[]
#     datarestore_dict ={}
#     for data in datastore["intents"]:
#         datarestore.append({
#             "client": data["client"],
#             "application":data["application"],
#             "module": data["module"],
#             "process": data["process"],
#             "subprocess": data["subprocess"],
#             "name": data["name"],
#             "tag": data["tag"],
#             "patterns": [i.lower().strip() for i in list(set(data["patterns"]))]
#         })
#     datarestore_dict["intents"]=datarestore
#     with open("test1.json", 'w') as f:
#         json.dump(datarestore_dict, f, indent=4)
#     return "Data cleaning Succesfully.... "
#
# print(data_clean())

###################################################################################
# header, output = client.request(twitterRequest, method="GET", body=None,
#                             headers=None, force_auth_header=True)
# with open("test1.json", 'wb') as f:
#     f.write(datarestore_dict)
#     f.close()
#  "additional_param": {
#             "button": [
#                 {
#                     "_id": 5,
#                     "entity_id": "6",
#                     "task_id": "2",
#                     "title": "Yes",
#                     "task": "#redirect-NewJoinerYes",
#                     "link": "",
#                     "utterance": "Yes"
#                 },
#                 {
#                     "_id": 6,
#                     "entity_id": "6",
#                     "task_id": "2",
#                     "title": "No",
#                     "task": "#redirect-NewJoinerNo",
#                     "link": "",
#                     "utterance": "No"
#                 }
#             ]
#         }
# context_data["chat_res"]["additional_param"]["button"] = button

# "chat_res": {
#         "reply_id": "",
#         "reply_text": [
#             {
#                 "type": "text",
#                 "sequence": "1",
#                 "value": "Are You new joiner"
#             }
#         ],
#         "reply_timestamp": "",
#         "additional_param": {
#             "button": [
#                 {
#                     "_id": 5,
#                     "entity_id": "6",
#                     "task_id": "2",
#                     "title": "Yes",
#                     "task": "#redirect-NewJoinerYes",
#                     "link": "",
#                     "utterance": "Yes"
#                 },
#                 {
#                     "_id": 6,
#                     "entity_id": "6",
#                     "task_id": "2",
#                     "title": "No",
#                     "task": "#redirect-NewJoinerNo",
#                     "link": "",
#                     "utterance": "No"
#                 }
#             ]

#
# with open("test.json", 'r') as f:
#     datastore = json.load(f)
# # print(selected_intents_list)
# # for data in selected_intents_list:
# #     for k, v in data.items():
# #         if str("Employee_Facing") in str(v):
# #             new_selected_list.append(data)
# #
# # print(new_selected_list)
# # # with open("test.json", 'w') as f:
# # #     json.dump(datarestore, f)
# datarestore=[]
# datarestore_dict ={}
# for data in datastore["intents"]:
#     datarestore.append({
#         "application":data["application"],
#         "module": data["module"],
#         "process": data["process"],
#         "subprocess": data["subprocess"],
#         "tag": data["tag"],
#         "patterns": list(set(data["patterns"]))
#     })
# datarestore_dict["intents"]=datarestore
# with open("test1.json", 'w') as f:
#     json.dump(datarestore_dict, f, indent=4)