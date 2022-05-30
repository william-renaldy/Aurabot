try:
    import pywhatkit as kt
    import time

except Exception as e:
    print(e)

def google_search(question):
    try:
        time.sleep(2)
        kt.search(question)
    except Exception as e:
        print(e)   