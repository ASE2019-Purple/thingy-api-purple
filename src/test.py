
import asyncio

import influx 
import mqtt 
import mysql

async def main():
    await influx.init_db()
    #create continuous query
    # influx.client.drop_continuous_query('average_temperature')
    # influx.client.drop_continuous_query('average_humidity')
    # influx.create_continuous_query("average_temperature", "Thingy-Temperature-Characteristic", "fe:84:88:ca:47:ca")
    # print(influx.get_list_continuous_query())
    # print(influx.get_thingy_average_characteristic("fe:84:88:ca:47:ca", "Thingy-Temperature-Characteristic", "2019-12-17"))
    # print(influx.get_thingy_average_characteristic("fe:84:88:ca:47:ca", "Thingy-Humidity-Characteristic", "2019-12-17"))
    #Get list retention policies
    # influx.create_retention_policy('one_month', '30d', True)
    # print(influx.get_list_retention_policies())
    # print(influx.get_characteristic_by_day('Thingy-Temperature-Characteristic', '2019-12-03'))
    # print(influx.get_characteristic_by_hours('Thingy-Temperature-Characteristic', '2019-12-03', '14:00', '15:00'))
    # await mysql.init_db()
    # print(mysql.get_all_plants())
    # print(mysql.get_plant_by_id(2))


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())



