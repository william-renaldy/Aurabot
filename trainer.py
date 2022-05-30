import json
import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
from tensorflow.python.framework import ops
import tflearn as tf
import pickle
import string
import time

def train_bot():
    with open("faq.json",encoding="utf8") as faq:
        data=json.load(faq)

    lemmatizer = WordNetLemmatizer()
    nltk.download("punkt")

    words=[]
    labels=[]
    docs_x=[]
    docs_y=[]

    for intent in data["intents"]:
        for question in intent["question"]:
            temp=nltk.word_tokenize(question)
            words.extend(temp)

            docs_x.append(temp)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])


    words=[lemmatizer.lemmatize(w.lower()) for w in words if w not in string.punctuation]

    words=sorted(list(set(words)))

    labels=sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x,doc in enumerate(docs_x):
        bag = []

        temp = [lemmatizer.lemmatize(w.lower()) for w in doc]

        for w in words:
            if w in temp:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])]=1

        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    print(len(training[0]))
    print(len(output[0]))


    ops.reset_default_graph()


    network = tf.input_data(shape=[None,len(training[0])])
    network = tf.fully_connected(network,160,activation="relu")
    network = tf.dropout(network,0.8)
    network = tf.fully_connected(network,160,activation="relu")
    network = tf.dropout(network,0.8)
    network = tf.fully_connected(network,len(output[0]),activation="softmax")
    network = tf.regression(network)

    model = tf.DNN(network)

    start = time.time()
    model.fit(training,output,n_epoch=150,batch_size=5, show_metric=True)
    end = time.time()
    model.save("model.tflearn")


    pickle.dump((words,labels,training,output),open("words.pkl","wb"))
    print(end-start)

if __name__=="__main__":
    train_bot()