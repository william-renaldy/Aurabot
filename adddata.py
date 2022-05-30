import json

class AddData():
    def __init__(self) -> None:
        pass

    def Add_data(self,question,tag):
        added = False
        with open("faq.json","r+",encoding="utf8") as file:
            data=json.load(file)

            for x in data["intents"]:
                x["question"] = [each_string.lower() for each_string in x["question"]] 
                if x["tag"] == tag:
                    if question.lower() not in x["question"]:
                        x["question"].append(question)
                        added = True
                        break

            file.seek(0)
            json.dump(data,file,indent=4)

        return added

    def Add_question(self,question,answer):
        with open("temp.txt","r") as f:
            tag = int(f.read())
            tag+=1

        with open("temp.txt","w") as f:
            f.writelines(str(tag))

        with open("faq.json","r+") as file:
            data = json.load(file)

            new_data = {"tag":str(tag),"question":[i for i in question],"answer":[i for i in answer]}
            data["intents"].append(new_data)

            file.seek(0)
            json.dump(data,file,indent=4)

        with open("static/questions.txt","r") as f:
            lines =  f.readlines()

        with open("static/questions.txt","w") as f:
            for line in lines:
                print(question[0],line.strip("\n"))
                if line.strip("\n")!=question[0]:
                    f.write(line)


def GetQuestions():

    with open("static/questions.txt","r") as f:
        data = []

        for text in f.readlines():
            data.append(text.replace("\n",""))

        return (data,len(data))