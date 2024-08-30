import psycopg2
import datetime
def insertDB(update_id, message_id,user_id,is_bot,first_name,last_name,chat_id,date,timestamp,text,photo):
    conn = psycopg2.connect(host="localhost", dbname="TeleBot",user="postgres",password="17102003",port=5432)
    cur = conn.cursor()
    cur.execute("""INSERT INTO users(user_id,is_bot,first_name,last_name) VALUES (%s,%s,%s,%s) ON CONFLICT (user_id) DO NOTHING
            """,(user_id,is_bot,first_name,last_name,))
    cur.execute("""INSERT INTO chats(chat_id,first_name,last_name) VALUES (%s,%s,%s) ON CONFLICT (chat_id) DO NOTHING
            """,(chat_id,first_name,last_name,))
    cur.execute("""INSERT INTO received_messages(message_id,chat_id,user_id,text) VALUES (%s,%s,%s,%s) 
            """,(message_id,chat_id,user_id,date,))
    cur.execute("""INSERT INTO sent_messages(message_id,chat_id,user_id,text,photo) VALUES (%s,%s,%s,%s,%s) 
            """,(message_id,chat_id,user_id,text,photo,))
    cur.execute("""INSERT INTO updates(update_id,message_id,user_id,chat_id,date) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (update_id) DO NOTHING
            """,(update_id,message_id,user_id,chat_id,datetime.datetime.fromtimestamp(timestamp),))
    conn.commit()
    cur.close()
    conn.close()

#insertDB(1214141,343353,42424,'False','alex','nguyen',14353533,'2024-02-18',datetime.datetime.fromtimestamp(1724724239),'i dont know','this is a picture')
#insertPage('100001')
#insertMessage('10001','103131','100001','1234','123141 etgrhr')