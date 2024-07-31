from aiogram import F, Router
from aiogram.types import Message
from aiogram.utils.formatting import Text, Bold
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from aiogram.filters.command import CommandObject, Command

from parser import find_abiturient

router = Router()
directions = {
        "btn1": "Разработка цифровых продуктов (программа реализуется на "
        "английском языке)",
        "btn3": "Разработка цифровых продуктов",
        "btn5": "Современная разработка программного обеспечения",
}

urls = {
    "Разработка цифровых продуктов (программа реализуется на "
    "английском языке)": "https://abiturient.kpfu.ru/entrant/abit_entrant"
    "_originals_list?p_open=&p_level=1&p_faculty=47&p_speciality=2021&p_i"
    "nst=0&p_typeofstudy=1",
    "Разработка цифровых продуктов": "https://abiturient.kpfu.ru/entrant/abit"
    "_entrant_originals_list?p_open=&p_level=1&p_faculty=47&p_speciality=1435"
    "&p_inst=0&p_typeofstudy=1",
    "Современная разработка программного обеспечения": "https://abiturient.kp"
    "fu.ru/entrant/abit_entrant_originals_list?p_open=&p_level=1&p_faculty=47"
    "&p_speciality=1416&p_inst=0&p_typeofstudy=1",
}
user_data = {}


# Хэндлер команды старт
@router.message(F.text, Command("start"))
async def cmd_start(message: types.Message):
    content = Text(
        "Привет, ",
        Bold(message.from_user.full_name), '!\n',
        "Чтобы увидеть список всех команд, введи ", Bold("/help"),
    )
    await message.answer(**content.as_kwargs())


@router.message(Command("help"))
async def cmd_help(message: Message):
    content = Text(
        Bold("Список доступных команд: \n"),
        "Сначала введите снилс и выберите направление\n",
        Bold("/snils"), " <snils_id> - ввод снилса\n",
        Bold("/select"), " - выбор направления\n",
        Bold("/info"), " - информация о введенных данных\n",
        Bold("/find"), " - найти себя в списке по снилсу\n",
    )
    await message.answer(**content.as_kwargs())


@router.message(Command("select"))
async def cmd_select(message: Message):
    builder = InlineKeyboardBuilder()
    buttons = []
    for cbdata, name in directions.items():
        buttons.append(types.InlineKeyboardButton(
            text=name,
            callback_data=cbdata)
        )
    builder.row(*buttons, width=1)
    await message.answer("Выберите направление",
                         reply_markup=builder.as_markup())


# Другая клавиатура
# @router.message(Command("select_list"))
# async def cmd_select(message: Message):

#     kb = [[types.KeyboardButton(text=i)] for i in directions]
#     keyboard = types.ReplyKeyboardMarkup(keyboard=kb, one_time_keyboard=True)
#     await message.answer('список:\n', reply_markup=keyboard)

@router.callback_query(F.data.startswith("btn"))
async def send_reply(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    direction = directions[callback.data]
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]["direction"] = direction
    await callback.message.edit_text("Направление выбрано")


@router.message(Command("snils"))
async def cmd_snils(
    message: Message,
    command: CommandObject
):
    # Если не переданы никакие аргументы, то
    # command.args будет None
    if command.args is None:
        await message.answer(
            "Не передан снилс"
        )
        return
    try:
        snils_id = command.args
        user_id = message.from_user.id
        if user_id not in user_data:
            user_data[user_id] = {}
        user_data[user_id]["snils"] = snils_id.replace(' ', '-')
        await message.answer("Снилс сохранён")
    except BaseException:
        await message.answer('Ошибка')


def print_user(user_id):
    user = user_data[user_id]
    direction = user["direction"] if "direction" in user else ""
    snils = user["snils"] if "snils" in user else ""
    return f"Ваш снилс: {snils}, ваше направление: {direction}"


@router.message(Command("info"))
async def cmd_info(message: Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        await message.answer("Вас нет в базе")
    else:
        await message.answer(print_user(user_id))


@router.message(Command("find"))
async def cmd_find(message: Message):
    user_id = message.from_user.id
    if user_id not in user_data or "direction" not in user_data[user_id] or \
       "snils" not in user_data[user_id]:
        await message.answer("Вы не ввели снилс или не выбрали направление")
        return
    await message.answer(find_abiturient(user_data[user_id]["snils"],
                                         urls[user_data[user_id]["direction"]])
                         )
