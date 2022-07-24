from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.keyboards.inline import menu_list_keyboard
from tgbot.load_all import _


async def start_menu(message: types.Message, list_items, text, item_type):
    """ Return list items """
    markup = menu_list_keyboard(list_items, 10, item_type)
    await message.answer(text, reply_markup=markup)


async def list_pagination(call: types.CallbackQuery, state: FSMContext, item_type):
    """ Pagination for menu """
    step = int(call.data.replace("step:", ""))
    data = await state.get_data()
    list_items = data.get("list_items")

    markup = menu_list_keyboard(list_items, step, item_type)
    await call.message.edit_reply_markup(reply_markup=markup)


async def cannot_find(call: types.CallbackQuery):
    """ User get pop up that tell about problem """
    await call.answer(_("I can't get the data"), show_alert=True)


async def cancel_search(callback: types.CallbackQuery, state: FSMContext):
    """ Cancel search """
    state_name = state.get_state()
    if state_name is not None:
        await state.finish()


def register_common_search(dp: Dispatcher):
    dp.register_callback_query_handler(cannot_find, lambda x: x.data and x.data.startswith("step:"))


