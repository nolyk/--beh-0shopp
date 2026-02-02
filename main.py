import pydantic
print("DEBUG PYDANTIC VERSION:", pydantic.__version__)

import asyncio
import colorama

from tgbot.handlers import userRouter, adminRouter
from tgbot.data.loader import dp, bot, adButtonRouter, scheduler
from tgbot.data.config import DB, BotImages
from tgbot.middlewares import setup_middlewares
from tgbot.utils.utils import check_rates, check_contests, check_updates, clear_stats_day, clear_stats_week
from tgbot.utils.models import async_main

colorama.init()

async def load_photos_from_db():
    """Загружает фотки из БД"""
    try:
        settings = await DB.get_settings()
        if settings.photo_main_menu:
            BotImages.START_PHOTO = settings.photo_main_menu
        if settings.photo_support:
            BotImages.SUPPORT_PHOTO = settings.photo_support
        if settings.photo_buy:      
            BotImages.BUY_PHOTO = settings.photo_buy
    except Exception as e:
        print(f"Error loading photos from DB: {e}")

async def scheduler_start():
    scheduler.add_job(clear_stats_week, "cron", day_of_week="mon", hour=00)
    scheduler.add_job(clear_stats_day, "cron", hour=00)
    scheduler.add_job(check_rates, 'cron', hour=00)

async def main():
    # Запускаем настройку и проверку базы данных
    await async_main()
    
    # Загружаем фотки из БД
    await load_photos_from_db()
    
    # Запускаем задания
    loop = asyncio.get_event_loop()
    loop.create_task(check_contests())
    loop.create_task(check_rates())
    loop.create_task(check_updates())
    
    # Подключаем мидлвари к роутерам
    setup_middlewares(userRouter)
    setup_middlewares(adButtonRouter)
    setup_middlewares(adminRouter)
    
    # Запуск заданий
    await scheduler_start()
    scheduler.start()
    
    print(colorama.Fore.GREEN + "=====================================")
    print(colorama.Fore.RED + "bot Was Started")
    print(colorama.Fore.LIGHTBLUE_EX + "developer: https://t.me/nolyktg")
    print(colorama.Fore.GREEN + "=====================================" + colorama.Fore.RESET)
    
    # Удаляем ненужный нам вебхук
    await bot.delete_webhook(drop_pending_updates=True)
    
    # В дистпетчер включаем наши роутеры и запускаем бота
    dp.include_routers(userRouter, adminRouter, adButtonRouter)    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
