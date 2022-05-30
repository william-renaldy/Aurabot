import json
import nltk
from nltk.stem import WordNetLemmatizer
import pickle
from tensorflow.python.framework import ops
import tflearn as tf
import numpy as np
import random
import csv
import os

from adddata import AddData
from verifier import Verifier

add_data = AddData()
verify = Verifier()


class Predictor():
    def __init__(self) -> None:
        self.lemmatizer = WordNetLemmatizer()
        self.binary = pickle.load(open("words.pkl","rb"))

        self.words = self.binary[0]
        self.labels = self.binary[1]
        self.training = self.binary[2]
        self.output = self.binary[3]




        ops.reset_default_graph()

        network = tf.input_data(shape=[None,len(self.training[0])])
        network = tf.fully_connected(network,160,activation="relu")
        network = tf.dropout(network,0.8)
        network = tf.fully_connected(network,160,activation="relu")
        network = tf.dropout(network,0.8)
        network = tf.fully_connected(network,len(self.output[0]),activation="softmax")
        network = tf.regression(network)

        self.model = tf.DNN(network)

        self.model.load("model.tflearn")

        with open("faq.json",encoding="utf8") as faq:
            self.data=json.load(faq)


    def words_collector(self,text,words):
        bag = [0 for _ in range(len(words))]

        lemmatized = nltk.word_tokenize(text)
        lemmatized = [self.lemmatizer.lemmatize(words.lower()) for words in lemmatized]

        for word in lemmatized:
            for i,w in enumerate(words):
                if w==word:
                    bag[i]=1

        return np.array(bag)



    def chat(self,text):


        try:
            ext = [chr(i) for i in range(40,58)]
            ext.append("%")
            ext.remove(chr(44))
            
            expression = [i for i in text if i in ext]
            
            expression = "".join(expression)

            checker = ['+','-','*','/','%']

            if not any(check in expression for check in checker):
                raise Exception("String has no mathematical expression")

            answer  = eval(expression)
            review = "no"
            return (f"{expression} = {answer}",review,False)

        except ZeroDivisionError:
            review = False

            return("Cannot Divide by zero",review,False)

        except:
            pass
        


        with open("static/questions.txt","r") as f:
            if (f"\n{text}\n" in f.read()) or (f"\n{text}" in f.read()):
                answer = ["Sorry! I didn't get that, try again<br>Your thirst for knowledge will be fed by Google shortly","I didn't get that!<br>Your thirst for knowledge will be fed by Google shortly"]
                
                review = False

                return(random.choice(answer),review,False)


        answer=[]
        added = False

        with open("faq.json","r",encoding="utf8") as f:
            data=json.load(f)

            for i,x in enumerate(data["intents"]):
                if text in x["question"]:
                    answer = verify.verify(x["tag"])
                    if answer:
                        review = "no"
                        return (answer,review,added)
                    answer=x["answer"]
                    review = "no"
                    print(answer)

                    return(random.choice(answer),review,added)
                    

        result = self.model.predict([self.words_collector(text=text,words=self.words)])[0]

        result_index = np.argmax(result)
        tag = self.labels[result_index]

        print(result[result_index])

        if result[result_index] > 0.85:
            for tg in self.data["intents"]:
                if tg["tag"] == tag:
                    answer = verify.verify(tag=tag)
                    if answer:
                        review = "no"
                        return (answer,review,added)
                    answer = tg["answer"]
                    added = add_data.Add_data(text,tag)
                    review = "no"

        elif result[result_index] > 0.50:

            for tg in self.data["intents"]:
                if tg["tag"] == tag:
                    answer = verify.verify(tag=tag)
                    if answer:
                        review = "yes"
                        return (answer,review,added)
                    answer = tg["answer"]
                    self.save(text,tag)
                    review = "yes"

        else:
            answer = ["Sorry! I didn't get that<br>Your thirst for knowledge will be fed by Google shortly","I didn't get that!<br>Your thirst for knowledge will be fed by Google shortly","Your thirst for knowledge will be fed by Google shortly."]
            with open("static/questions.txt","a") as f:
                if os.path.getsize("static/questions.txt") != 0:
                    f.write("\n")
                f.write(f"{text}")
            review = False
            
        return (random.choice(answer),review,added)

    def save(self,text,tag):
        with open("temp.csv","w",newline="") as f:
            writer=csv.writer(f)
            writer.writerow((text,tag))