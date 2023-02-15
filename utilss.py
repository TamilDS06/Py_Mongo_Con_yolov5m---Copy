from pymongo import MongoClient
import numpy as np
import requests
import cv2
from PIL import Image
from api_call import api_log_in
import sys
from constant import constant
import json
import urllib
import time

def get_connection():
    try:
        client = None
        while True:
            if internet_connect():
                client = MongoClient(constant.connection_string)
                break
            else:
                print("Internet is interrupted @", time.strftime('%H-%M-%S'), "While connecting to MongoDb")
                time.sleep(constant.time_to_wait)
    except Exception as exception:
        print("Error occurred in get_connection method", exception.args)
    finally:
        return client

def convert_url_to_image(url):
    try:
        url = str(url)
        url = '{"url":'+'"'+url+'"'+'}'
        url = json.loads(url)
        im = None
        while True:
            if internet_connect():
                try:
                    im = np.asarray(Image.open(requests.get(url['url'], stream=True).raw))
                except:
                    print("URL is invalid")
                    pass
                break
            else:
                print("Internet is interrupted @", time.strftime('%H-%M-%S'), "While converting url to image")
                time.sleep(constant.time_to_wait)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    except Exception as exception:
        print("Error occurred in convert_url_to_image method", exception.args)
        pass
    finally:
        return im

def get_client_id():
    try:
        client_id = None
        while True:
            if internet_connect():
                response = api_log_in()
                if response is None:
                    continue
                break
            else:
                print("Internet is interrupted @", time.strftime('%H-%M-%S'), "While getting client_id")
                time.sleep(constant.time_to_wait)
        true = True
        false = False
        response = eval(response.text)
        if response["status"] == True and response["status_code"] == 200:
            token = response['token']
            client_id = response['client_id']
        else:
            print(response)
            sys.exit()
    except Exception as exception:
        print("Error occurred in get_client_id method", exception.args)
    finally:
        return client_id

def close_connection(get_db):
    try:
        while True:
            if internet_connect():
                get_db.close()
                print("Db connection closed successfully")
                break
            else:
                print("Internet is interrupted @", time.strftime('%H-%M-%S'), "While closing the db connection")
                time.sleep(constant.time_to_wait)
    except Exception as exception:
        print("Error occurred in get_client_id method", exception.args)

def internet_connect(host='http://google.com'): 
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False
    
def update_count_DB(ai_counts_collection, ai_counts_single_doc, update_count, is_processed):
    while True:
        if internet_connect():
            ai_counts_collection.update_one({'_id':ai_counts_single_doc['_id']},{'$set':{'count':str(update_count)}})
            ai_counts_collection.update_one({'_id':ai_counts_single_doc['_id']},{'$set':{'is_processed':is_processed}})
            print("count is: ", update_count)
            print("updating", ai_counts_single_doc['_id'])
            break
        else:
            print("Internet is interrupted @", time.strftime('%H-%M-%S'), "While updating the count")
            time.sleep(constant.time_to_wait)


    #         def update_count_DB(ai_counts_collection, ai_counts_single_doc, update_count, is_processed):
    # while True:
    #     if internet_connect():
    #         ai_counts_collection.update_one({'_id':ai_counts_single_doc['_id']},{'$set':{'count':str(update_count)}})
    #         ai_counts_collection.update_one({'_id':ai_counts_single_doc['_id']},{'$set':{'is_processed':is_processed}})
    #         print("count is: ", update_count)
    #         print("updating", ai_counts_single_doc['_id'])
    #         break
    #     else:
    #         print("Internet is interrupted @", time.strftime('%H-%M-%S'), "While updating the count")
    #         time.sleep(constant.time_to_wait)
        