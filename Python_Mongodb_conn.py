from load_model import load_model
from constant import constant
import cv2
from utilss import internet_connect, get_client_id, get_connection, convert_url_to_image, update_count_DB, close_connection
import time

def count_update():
    try:
        while True:
            if internet_connect():
                client_id = get_client_id()
                if client_id is None:
                    continue
                print("Client_ID : ",client_id)
                get_db = get_connection()
                print("Db connection created")
                break
            else:
                print("Internet is interrupted @", time.strftime('%H-%M-%S'), "While creating DB Connection & Client ID")
                time.sleep(constant.time_to_wait)
        while True:
            get_db_SmartVeo = get_db['SMARTVEO_CLIENT_'+str(client_id)]
            ai_counts_collection = get_db_SmartVeo["ai_counts"]
            ai_counts = ai_counts_collection.find({'is_processed':0})
            updated_record_count = 0
            update_count = 0
            for ai_counts_single_doc in ai_counts:
                update_count = get_count(ai_counts_single_doc['image'])
                is_processed = 2 if update_count == -1 else 1
                update_count_DB(ai_counts_collection, ai_counts_single_doc, update_count, is_processed)
                updated_record_count += 1
                if ai_counts.alive:
                    pass
                else:
                    print("Total updated document counts is ",updated_record_count)
                    time.sleep(15)
                    continue
    except Exception as exception:
        print("Error occurred during count_update method", exception.args)
    finally:
        close_connection(get_db)
        return update_count

def get_count(url):
    try:
        person_count = -1
        image = convert_url_to_image(url)
        if image is None:
            return person_count
        else:
            model = load_model()
            if model is None:
                return person_count
            result = model(image)
            result.pandas().xyxy[0].columns = ['xmin', 'ymin', 'xmax', 'ymax', 'confidence', 'clas', 'name']
        person_count = 0
        for xmin, ymin, xmax, ymax, confidence, clas, name in result.pandas().xyxy[0].itertuples(index=False):
            if clas == 0:
                person_count += 1
        print("Total persons in current frame", person_count)
    except Exception as exception:
        print("Error occurred in get_count method", exception.args)
    finally:
        return person_count