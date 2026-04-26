import asyncio  
from aiogram import Bot, Dispatcher
from hendller.base_function import my_router
from hendller.admin_ponel import admin_router
import os
TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)  
dp = Dispatcher()  


async def main():  
    await bot.delete_webhook(drop_pending_updates=True)
    print("bot start")
    dp.include_routers(my_router,admin_router) 
    await dp.start_polling(bot)  
  
  
  
if __name__ == "__main__":  
    try:  
        asyncio.run(main())
    except KeyboardInterrupt:  
        print("bot exit")
