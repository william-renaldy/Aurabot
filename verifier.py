import pyjokes
from datetime import datetime
from datetime import date
import socket

class Verifier():
    def __init__(self) -> None:
        self.loader = ("time","day","date","month","year","jokes","ip - 2")

    def time(self):
        current_time = datetime.today().strftime("%I:%M %p")

        return f"It's {current_time}"


    def day(self):
        current_day = datetime.now().strftime("%A")

        return f"Today is {current_day}"


    def date(self):
        current_date = datetime.now().strftime("%d/%m/%Y")

        return f"Today is {current_date}"

    def month(self):
        current_month = datetime.now().strftime("%B")

        return current_month

    def year(self):
        current_year = date.today().year

        return current_year


    def jokes(self):

        joke = pyjokes.get_joke(language="en",category="all")

        return joke

    def ip(self):
        host = socket.gethostname()
        
        ip_address = socket.gethostbyname(host)

        return ip_address




    def verify(self,tag):
        if tag in self.loader:
            if tag == "time":
                return self.time()

            if tag == "day":
                return self.day()

            if tag == "date":
                return self.date()

            if tag == "month":
                return self.month()

            if tag == "year":
                return self.year()

            if tag == "jokes":
                return self.jokes()

            if tag == "ip - 2":
                return self.ip()