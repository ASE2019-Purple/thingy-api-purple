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

def insert_thingy(mac_address, location):
    with connection.cursor() as cursor:
        sql = 'INSERT INTO `thingys` (mac_address, location) VALUES(%s, %s)'
        cursor.execute(sql,(mac_address, location))
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
            "start_date": plant[5],
            "thingy_id":plant[6]
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

def get_thingy_by_id(id):
    result = None
    with connection.cursor() as cursor:
        sql = 'SELECT `*` FROM thingys WHERE id=%s'
        cursor.execute(sql, (id))
        result = cursor.fetchone()
        cursor.close()

    if result == None:
        return result
        
    obj = {
        "id":result[0],
        "mac_address":result[1],
        "location":result[2],
    }
    return obj

def select_properties():
    result = None
    with connection.cursor() as cursor:
        sql = 'SELECT `*` FROM properties'
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

    if result == None:
        return result

    properties = []
    for property in result:
        obj = {
            "id":property[0],
            "name":property[1],
            "characteristic":property[2],
            "type":property[3],
            "unit":property[4],
            "readOnly":property[5],
        }
        properties.append(obj)
    return properties

def select_property_by_name(name):
    result = None
    with connection.cursor() as cursor:
        sql = 'SELECT `*` FROM properties WHERE name=%s'
        cursor.execute(sql, (name))
        result = cursor.fetchone()
        cursor.close()

    if result == None:
        return result
        
    obj = {
        "id":result[0],
        "name":result[1],
        "characteristic":result[2],
        "type":result[3],
        "unit":result[4],
        "readOnly":result[5],
    }
    return obj