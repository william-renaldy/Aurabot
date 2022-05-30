#This will not run on online IDE
import requests
from bs4 import BeautifulSoup

URL = "https://www.edx.org/learn/mechanical-engineering"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html.lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
print(soup.prettify())
