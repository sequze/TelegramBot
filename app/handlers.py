from aiogram import F, Router
from aiogram.types import Message
from aiogram.utils.formatting import Text, Bold
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from aiogram.filters.command import CommandObject, Command

router = Router()
directions = {
        "btn1": "Разработка цифровых продуктов (программа реализуется на "
        "английском языке)",
        "btn2": "Разработка цифровых продуктов (программа реализуется на "
        "английском языке) (для иностранных граждан)",
        "btn3": "Разработка цифровых продуктов",
        "btn4": "Разработка цифровых продуктов "
        "(для приема иностранных граждан)",
        "btn5": "Современная разработка программного обеспечения",
        "btn6": "Современная разработка программного обеспечения  (для приема "
        "иностранных граждан)"
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
        Bold("/find"), " <snils_id> - найти себя в списке по снилсу\n",
        Bold("/select_list"), " - выбрать направление/вуз\n",
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
        user_data[user_id]["snils"] = snils_id
        await message.answer(snils_id.replace('-', '').replace(' ', ''))
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
