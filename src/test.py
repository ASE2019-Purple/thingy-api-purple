
import asyncio

import db 
import mqtt 

async def main():
    await db.init_db()
    #Get list retention policies
    # db.create_retention_policy('one_month', '30d', True)
    # print(db.get_list_retention_policies())
    # print(db.get_characteristic_by_day('Thingy-Temperature-Characteristic', '2019-12-03'))
    print(db.get_characteristic_by_hours('Thingy-Temperature-Characteristic', '2019-12-03', '14:00', '15:00'))


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())



