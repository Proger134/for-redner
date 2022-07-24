import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.db_api.user_commands import get_all_users, add_user, get_users_count
from tgbot.keyboards.admin_inline import apply_mailing_keyboard
from tgbot.misc.bot_commands import set_admin_bot_commands
from tgbot.misc.states import FSMMailing


async def admin_start(message: Message):
    await message.answer("Hello, admin!")
    await add_user(telegram_id=message.from_user.id, language="en")
    await set_admin_bot_commands(message.bot, message.from_user.id)


async def get_count_users(message: Message):
    users_count = await get_users_count()
    await message.answer(f"Count users: {users_count}")


async def mailing(message: Message):
    await message.answer("Enter text for mailing")
    await FSMMailing.text.set()


async def get_mailing_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await FSMMailing.next()
    await message.answer(f"<b>Mailing text:</b>\n\n{message.text}", disable_web_page_preview=True)
    await message.answer("Would you like to mail this text?", reply_markup=apply_mailing_keyboard)


async def apply_mailing(call: CallbackQuery, state: FSMContext):
    answer = call.data.split(":")[1]
    data = await state.get_data()
    text = data.get("text")

    if answer == "yes":
        users = await get_all_users(language="en")
        for user in users:
            await call.bot.send_message(chat_id=user.telegram_id, text=text, disable_web_page_preview=True)
            await asyncio.sleep(0.3)
    else:
        await call.message.answer("Ok")

    await state.finish()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["admin_start"], state="*", is_admin=True)
    dp.register_message_handler(get_count_users, commands=["count_users"], state="*", is_admin=True)

    dp.register_message_handler(mailing, commands=["mailing"], is_admin=True, state="*")
    dp.register_message_handler(get_mailing_text, state=FSMMailing.text)
    dp.register_callback_query_handler(apply_mailing, lambda x: x.data and x.data.startswith("mailing:"), state=FSMMailing.apply)

