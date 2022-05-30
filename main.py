from flask import Flask,render_template,request,jsonify,redirect, url_for
from threading import Thread
import random
import csv
import os
import json


from predictor import Predictor
from speech import SpeechToText,TextToSpeech
from adddata import AddData,GetQuestions
import search
from secret_code import Code



add_data = AddData()

chatbot = Predictor()
speech_to_text = SpeechToText()
app = Flask(__name__)


status = 0
key = ""
access = False
editing_done = False

@app.route("/")
def home():
    return render_template("chatbot.html")

@app.route("/speak",methods=["POST"])
def speaker():
    global status

    msg = speech_to_text.Speech_to_text()

    if msg:
        result,status,added = chatbot.chat(msg)
        if status==False:
            search_thread(msg)
        say_text(result)
        run_code(added)
        return jsonify(msg,result,status)
    else:
        result = random.choice(["Sorry! I didn't get that, try again","I didn't get that!"])
        say_text(result)
        return jsonify("...",result,status)


@app.route("/get",methods=["POST"])
def chat():
    global status



    msg = request.form["msg"]

    result,status,added = chatbot.chat(msg)
    if status==False:
        search_thread(msg)
    run_code(added)
    return jsonify(result,status)


@app.route("/suggestion",methods=["POST"])
def rating():

    rate = request.form["res"]
    if rate == "yes":
        with open("temp.csv","r+") as f:
            reader=csv.reader(f)
            
            for row in reader:
                file=row

            f.truncate(0)
        added = add_data.Add_data(file[0],file[1])
        run_code(added)

    else:
        with open("temp.csv","r+") as f:
            reader=csv.reader(f)
            
            for row in reader:
                file=row
            
            f.truncate(0)

        with open("static/questions.txt","a") as f:
            if os.path.getsize("static/questions.txt") != 0:
                f.write("\n")
            f.write(f"{file[0]}")

        search_thread(file[0])

        return "Your thirst for knowledge will be fed by Google shortly"

    return rate






@app.route("/admin-login",methods=["POST","GET"])
def admin_login():
    global key,access

    access = False

    if request.method == "GET":
        code_generator = Code()
        code,key = code_generator.code_generator()
        print(key)

        return render_template("login.html",code=code)

    elif request.method == "POST":
        entered_key = request.form['key']
        print(entered_key)

        if entered_key == key:
            access = True
            return redirect(url_for('editing'))

        else:
            return redirect(url_for("admin_login"))

@app.route("/editing", methods=["POST","GET"])
def editing():
    global access
    if access:
        question,length = GetQuestions()
        return render_template("editing.html",length = length,question = question)
    else:
        return redirect(url_for("admin_login"))


@app.route("/editing/<question>",methods=["POST","GET"])
def answer_provider(question):
    if request.method == "POST":
        return render_template("answer.html",questions=question)
    else:
        return redirect(url_for("admin_login"))


@app.route("/done",methods = ["POST","GET"])
def done_answer():
    global editing_done

    if request.method == "POST":

        question = request.form["ques"]
        answer = request.form["ans"]

        question = json.loads(question)
        answer = json.loads(answer)

        print(question,answer)

        add_data.Add_question(question=question,answer=answer)

        
        
        editing_done = True

        return render_template("done.html")

    else:
        
        if editing_done:
            editing_done = False
            return render_template("done.html")
        else:
            return redirect(url_for("admin_login"))
        








def speak(app,text):
    with app.app_context():
        TextToSpeech().Text_to_speech(text)


def say_text(text):
    thread = Thread(target=speak,args=[app,text])
    thread.start()
    return thread


def run_code(added):
    if added and random.randint(0,10)==0:
        thread = Thread (target=reloader,args=[app])

        thread.start()
        return thread

def searcher(app,question):
    with app.app_context():
        search.google_search(question=question)
        
def search_thread(question):
    thread = Thread(target=searcher,args=[app,question])
    thread.start()

    return thread

def reloader(app):

    return
    global chatbot
    with app.app_context():
        import trainer
        trainer.train_bot()
        del chatbot
        chatbot = Predictor()



if __name__ == "__main__":
    app.run(debug=True)