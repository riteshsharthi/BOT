# # # Define the documents
# # doc_trump = "Mr. Trump became president after winning the political election. Though he lost the support of some republican friends, Trump is friends with President Putin"
# #
# # doc_election = "President Trump says Putin had no political interference is the election outcome. He says it was a witchhunt by political parties. He claimed President Putin is a friend who had nothing to do with the election"
# #
# # doc_putin = "Post elections, Vladimir Putin became President of Russia. President Putin had served as the Prime Minister earlier in his political career"
# #
# # documents = [doc_trump, doc_election, doc_putin]
# #
# # # Scikit Learn
# # from sklearn.feature_extraction.text import CountVectorizer
# # import pandas as pd
# #
# # # Create the Document Term Matrix
# # count_vectorizer = CountVectorizer(stop_words='english')
# # count_vectorizer = CountVectorizer()
# # sparse_matrix = count_vectorizer.fit_transform(documents)
# #
# # # OPTIONAL: Convert Sparse Matrix to Pandas Dataframe if you want to see the word frequencies.
# # doc_term_matrix = sparse_matrix.todense()
# # df = pd.DataFrame(doc_term_matrix,
# #                   columns=count_vectorizer.get_feature_names(),
# #                   index=['doc_trump', 'doc_election', 'doc_putin'])
# #
# # print(df)
# #
# # from sklearn.metrics.pairwise import cosine_similarity
# # print(cosine_similarity(df, df))
#
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
# from keras.models import Model
# from keras.layers import LSTM, Activation, Dense, Dropout, Input, Embedding
# from keras.optimizers import RMSprop
# from keras.preprocessing.text import Tokenizer
# from keras.preprocessing import sequence
# from keras.utils import to_categorical
# from keras.callbacks import EarlyStopping
# %matplotlib inline