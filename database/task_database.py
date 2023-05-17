import aiosqlite
import asyncio

idd = 1


class AioSQLiteClient:

    async def __aenter__(self):
        self.db = await aiosqlite.connect('base.db')
        return self

    async def __aexit__(self, *args):
        await self.db.close()

    async def get_data(self, user_id):
        cursor = await self.db.execute("SELECT * FROM users WHERE user_id == ?", (user_id,))
        row = await cursor.fetchone()
        return row


class GetData:

    def __init__(self, user_id):
        self.user_id = user_id
        self.cont = []

    async def get_row(self):
        async with AioSQLiteClient() as BD_Name:
            data = await BD_Name.get_data(self.user_id)
            # if data:
            #     self.cont.append('\nBD_Name.CSV'
            #                      '\n├ Телефон: {}'
            #                      '\n├ ФИО: {}'.format(data[1], data[3]))
            print(data)
            return self.cont


asyncio.run(GetData('1').get_row())
