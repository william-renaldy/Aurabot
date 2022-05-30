import random


class Code():
    def __init__(self) -> None:
        self.variables='''ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()-_=+{}[]|\:;"'<>,./?`~'''
        
        self.code=""
        self.key=""

    def code_generator(self):
        for _ in range(8):
            self.code+=random.choice(self.variables)

        random.seed(self.code)
        for _ in range(8):
            self.key+=random.choice(self.variables)

        return (self.code,self.key)