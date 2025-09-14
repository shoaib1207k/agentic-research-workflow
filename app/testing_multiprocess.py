from time import time
from datetime import datetime
import requests
import threading

def send_topic(topic):
    print("*-"*100)
    start = time()
    response = requests.post("http://localhost:8000/research-topic", params={"topic": topic})
    end = time()

    start_str = datetime.fromtimestamp(start).strftime("%H:%M:%S.%f")[:-3]
    end_str = datetime.fromtimestamp(end).strftime("%H:%M:%S.%f")[:-3]

    print(f"Topic: {topic}, Sent: {start_str}, Received: {end_str}, Status: {response.status_code}")
    print("*-"*100)

topics = ["AI Ethics", "Blockchain", "Genomics"]

threads = []
for topic in topics:
    t = threading.Thread(target=send_topic, args=(topic,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()