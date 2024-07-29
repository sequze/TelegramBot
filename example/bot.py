import asyncio
from aiogram import Bot, Dispatcher
from handlers import questions, different_types, group_games


# Запуск бота
async def main():
    bot = Bot(token="7270785496:AAGqXN553OnrNYaxtXy7X76Ixuu2pdNNyR8")
    dp = Dispatcher()
    dp.include_routers(group_games.router,questions.router, 
                       different_types.router,
                       )
    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
