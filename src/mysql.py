import pymysql.cursors
import os


connection = None

async def init_db():
    global connection
    connection = pymysql.connect(host="35.205.33.242",
                             user="purple",
                             password="purple",
                             db="purple",
                             charset='utf8mb4')

def insert_thingy(mac_address):
    with connection.cursor() as cursor:
        sql = 'INSERT INTO `thingys` (mac_address) VALUES(%s)'
        cursor.execute(sql,(mac_address))
        connection.commit()
        cursor.close()


def insert_plant(name, nb_sunny_days, nb_rainy_days, watering_interval_days, thingy_id):
    #insert data into the database
    with connection.cursor() as cursor:
        sql = 'INSERT INTO `plants` (name, nb_sunny_days, nb_rainy_days, watering_interval_days) VALUES(%s,%s,%s,%s,%s)'
        cursor.execute(sql,(name, nb_sunny_days, nb_rainy_days, watering_interval_days, thingy_id))
        connection.commit()
        cursor.close()

def get_all_plants():
    result = None
    with connection.cursor() as cursor:
        sql = "SELECT `*` FROM plants"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

    if result == None:
        return result

    plants = []
    for plant in result:
        obj = {
            "id":plant[0],
            "name":plant[1],
            "nb_sunny_days":plant[2],
            "nb_rainy_days":plant[3],
            "watering_interval_days":plant[4],
            "thingy_id":plant[5]
        }
        plants.append(obj)

    return plants

def get_plant_by_id(id):
    result = None
    with connection.cursor() as cursor:
        sql = "SELECT `*` FROM plants WHERE id=%s"
        cursor.execute(sql,(id))
        result = cursor.fetchone()
        cursor.close()

    if result == None:
        return result
        
    obj = {
        "id":result[0],
        "name":result[1],
        "nb_sunny_days":result[2],
        "nb_rainy_days":result[3],
        "watering_interval_days":result[4],
        "thingy_id":result[5]
    }
    return obj