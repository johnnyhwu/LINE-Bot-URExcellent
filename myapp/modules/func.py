from django.conf import settings
from myapp.models import text_collection

from linebot import LineBotApi
from linebot.models import TextSendMessage

import random
import os
import psycopg2
import hashlib



line_bot_api = LineBotApi(settings.CHANNEL_ACCESS_TOKEN)


def send_text(event):
    
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM text_collection ORDER BY random() LiMIT 1;")
    records = cursor.fetchall()
    result = records[0][0]
    
    conn.commit()
    cursor.close()
    conn.close()
    
    
    return line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))


def delete_record_sql(id):
    
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM text_collection WHERE id=%s;", (id, ))
        status = 1
    except Exception:
        status = 0
        
    conn.commit()
    cursor.close()
    conn.close()
    
    return status
    
    
def add_record_sql(text):
    
    text_id = int(hashlib.sha256(text.encode('utf-8')).hexdigest(), 16) % 10**8
    
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO text_collection(text, id) VALUES (%s, %s);", (text, text_id))
        status = 1
    except Exception:
        status = 0
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return [status, text_id]


def read_record_sql():
    
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    records = None
    
    try:
        cursor.execute("SELECT * FROM text_collection;")
        records = cursor.fetchall()
    except Exception:
        pass
    
    
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return records
    
    