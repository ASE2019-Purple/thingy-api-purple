from datetime import datetime
import pymysql.cursors
import os

connection = None


async def init_db():
    global connection
    connection = pymysql.connect(
        host="35.205.33.242",
        user="purple",
        password="purple",
        db="purple",
        charset="utf8mb4",
    )


def select_plants():
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
            "id": plant[0],
            "name": plant[1],
            "optimal_temperature": plant[2],
            "optimal_humidity": plant[3],
            "watering_interval_days": plant[4],
            "start_date": plant[5].strftime("%Y-%m-%d"),
            "thing_id": plant[6],
        }
        plants.append(obj)

    return plants


def select_plant_by_id(id):
    result = None
    with connection.cursor() as cursor:
        sql = "SELECT `*` FROM plants WHERE id=%s"
        cursor.execute(sql, (id))
        result = cursor.fetchone()
        cursor.close()

    if result == None:
        return result

    obj = {
        "id": result[0],
        "name": result[1],
        "optimal_temperature": result[2],
        "optimal_humidity": result[3],
        "watering_interval_days": result[4],
        "start_date": result[5].strftime("%Y-%m-%d"),
        "thing_id": result[6],
    }
    return obj


def insert_plant(plant):
    start_date = datetime.now().strftime("%Y-%m-%d")
    with connection.cursor() as cursor:
        sql = "INSERT INTO `plants` (name, optimal_temperature, optimal_humidity, watering_interval_days, start_date, thing_id) VALUES(%s,%s,%s,%s,%s,%s)"
        cursor.execute(
            sql,
            (
                plant['name'],
                plant['optimal_temperature'],
                plant['optimal_humidity'],
                plant['watering_interval_days'],
                start_date,
                plant['thing_id']
            ),
        )
        id = cursor.lastrowid
        connection.commit()
        cursor.close()
        return id


def update_plant_by_id(plant):
    start_date = datetime.now().strftime("%Y-%m-%d")
    with connection.cursor() as cursor:
        sql = "UPDATE `plants` SET name=%s, optimal_temperature=%s, optimal_humidity=%s, watering_interval_days=%s, start_date=%s, thing_id=%s WHERE id=%s"
        cursor.execute(
            sql,
            (
                plant['name'],
                plant['optimal_temperature'],
                plant['optimal_humidity'],
                plant['watering_interval_days'],
                start_date,
                plant['thing_id'],
                plant['plant_id']
            ),
        )
        id = cursor.lastrowid
        connection.commit()
        cursor.close()
        return id


def delete_plant_by_id(id):
    result = None
    with connection.cursor() as cursor:
        sql = "DELETE FROM plants WHERE id=%s"
        affectedRows = cursor.execute(sql, (id))
        succes = affectedRows == 1
        if succes: connection.commit()
        else: connection.fallback()
        cursor.close()
        return succes
     

def select_things():
    result = None
    with connection.cursor() as cursor:
        sql = "SELECT `*` FROM things"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

    if result == None:
        return result

    things = []
    for thing in result:
        obj = {"id": thing[0], "mac_address": thing[1], "location": thing[2]}
        things.append(obj)

    return things


def select_thing_by_id(id):
    result = None
    with connection.cursor() as cursor:
        sql = "SELECT `*` FROM things WHERE id=%s"
        cursor.execute(sql, (id))
        result = cursor.fetchone()
        cursor.close()

    if result == None:
        return result

    obj = {"id": result[0], "mac_address": result[1], "location": result[2]}
    return obj
    

def insert_thing(thing):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `things` (mac_address, location) VALUES(%s, %s)"
        cursor.execute(sql, (thing['mac_address'], thing['location']))
        id = cursor.lastrowid
        connection.commit()
        cursor.close()
        return id


def delete_thing_by_id(id):
    with connection.cursor() as cursor:
        sql = "DELETE FROM things WHERE id=%s"
        affectedRows = cursor.execute(sql, (id))
        succes = affectedRows == 1
        if succes: connection.commit()
        else: connection.rollback()
        cursor.close()
        return succes


def select_properties():
    result = None
    with connection.cursor() as cursor:
        sql = "SELECT `*` FROM properties"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

    if result == None:
        return result

    properties = []
    for property in result:
        obj = {
            "id": property[0],
            "name": property[1],
            "characteristic": property[2],
            "type": property[3],
            "unit": property[4],
            "readOnly": property[5],
        }
        properties.append(obj)
    return properties


def select_property_by_name(name):
    result = None
    with connection.cursor() as cursor:
        sql = "SELECT `*` FROM properties WHERE name=%s"
        cursor.execute(sql, (name))
        result = cursor.fetchone()
        cursor.close()

    if result == None:
        return result

    obj = {
        "id": result[0],
        "name": result[1],
        "characteristic": result[2],
        "type": result[3],
        "unit": result[4],
        "readOnly": result[5],
    }
    return obj
