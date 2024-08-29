from flask import Flask, request, Response 
from flask import request
from dotenv import load_dotenv
import requests
import os
import re
import datetime
import db
import threading
import queue
load_dotenv
#TOKEN = os.getenv("BOT_TOKEN")
TOKEN ='7464937134:AAHnO8ORZhYnrIITWIMP5Bcu1QkqHmuOLbQ'
print(TOKEN)
#db.insertDB(1214141,343353,42424,'False','alex','nguyen',14353533,'2024-02-18',datetime.datetime.fromtimestamp(1724724239),'i dont know','this is a picture')

app = Flask(__name__)
def check_date_format(date_text):
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    if re.match(pattern, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
            #print("Định dạng và giá trị ngày tháng hợp lệ:", date_text)
        except ValueError:
             return False
            #print("Giá trị ngày tháng không hợp lệ. Vui lòng nhập lại.")
        
def get_moon_description(date):
    url = f"https://api.nasa.gov/planetary/apod?date={date}&api_key=xGNab3f80aF6texedcxx6zC0uYXH8h3HmU7AStTU"
    response = requests.get(url)
    data = response.json()
    return data
task_queue = queue.Queue()
def worker():
    while True:
        task = task_queue.get()
        if task is None: # Kiểm tra nếu có tín hiệu dừng
            break
        print(task)
        db.insertDB(task['update_id'],task['update_id'],task['user_id'],task['is_bot'],task['first_name'],task['last_name'],
                     task['chat_id'],task['date'],datetime.datetime.fromtimestamp(task['timestamp']),task['text'],task['photo'])
        task_queue.task_done()

# Khởi tạo các luồng làm việc
num_threads = 5
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=worker)
    thread.start()
    threads.append(thread)
@app.route('/', methods=['POST'])

def post_example():
    if request.method == 'POST':
        msg = request.get_json()  
        print("Message: ",msg)

        try:
            print("There is a text")
            chat_id = msg['message']['chat']['id']
            date = msg['message']['text'] 
            update_id = msg['update_id']
            message_id = msg['message']['message_id']
            user_id = msg['message']['from']['id']
            is_bot = msg['message']['from']['is_bot']
            first_name = msg['message']['from']['first_name']
            last_name = msg['message']['from']['last_name']
            timestamp = msg['message']['date']
            print(chat_id)
            print(date)
            if 1:
                data = get_moon_description(date)    
                text = data['explanation']     
                photo = data['url']
                print(text)
                print(photo)
                task_queue.put({'update_id':update_id, 
                                'message_id':message_id,
                                'user_id':user_id,
                                'is_bot':is_bot,
                                'first_name':first_name, 
                                'last_name':last_name,
                                'chat_id':chat_id, 
                                'date':date,
                                'timestamp':timestamp,
                                'text':text,
                                'photo':photo})
                urlMess = f'https://api.telegram.org/bot{TOKEN}/sendMessage' 
                urlPhoto = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
                payload = {
                    'chat_id': chat_id,
                    'photo': photo,
                    'caption': f'Picture in {date}'
                    }
                r = requests.post(urlPhoto, json=payload)
                payload = {
                    'chat_id': chat_id,
                    'text': text
                    }
                
                r = requests.post(urlMess, json=payload)
                if r.status_code == 200:
                    return Response('ok', status=200)
                else: 
                    return Response('Failed to send message to Telegram', status=500)
            else:
                payload = {
                    'chat_id': chat_id,
                    'text': "Đã xảy ra lỗi, vui lòng kiểm tra lại định dạng và kiểm tra về dữ liệu nhập vào"
                    }

                r = requests.post(urlMess, json=payload)   
        except:
            print("No text found")

        return Response('ok', status=200)
def shutdown_threads(exception=None):
    for i in range(num_threads):
        task_queue.put(None)
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=4000, use_reloader=False)
    finally:
        shutdown_threads()



#D:\CodeBlocks\C-C++\.vscode\.vscode\Intern\telegram\kaggle\working\wandb\run-20240814_022848-9mk12mm1\files\requirements.txt