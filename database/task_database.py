import asyncio
import aiosqlite


async def set_datas(user_id: int, username: str):
    async with aiosqlite.connect(r"C:\my_projects\NapominalkaBot\database\base.db") as db:
        try:
            await db.execute("INSERT INTO users(user_id, username) VALUES(?, ?)", (user_id, username))
            await db.commit()
        except Exception as err:
            print(err)


async def get_all_users_id():
    async with aiosqlite.connect(r"C:\my_projects\NapominalkaBot\database\base.db") as db:
        cursor = await db.execute("SELECT * FROM users")
        users = await cursor.fetchall()
        users = [row[0] for row in users]
        return users

asyncio.run(get_all_users_id())
