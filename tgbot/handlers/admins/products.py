from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.types.input_file import FSInputFile

from tgbot.data.loader import adminRouter
from tgbot.data.config import BotButtons, BotConfig, DB
from tgbot.data.config import BotTexts as BTs
from tgbot.utils import utils
from tgbot.states import adminStates
from tgbot.utils import models

from traceback import print_exc
import os


@adminRouter.callback_query(F.data == "products_manage")
async def products_manage(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    await call.message.edit_text(BotTexts.ADMIN_TEXTS.products_manage_text, 
                                 reply_markup=BotButtons.ADMIN_INLINE.products_manage(BotTexts).as_markup())
    

### Categories
@adminRouter.callback_query(F.data == "add_category")
async def add_category(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    await call.message.edit_text(BotTexts.ADMIN_TEXTS.add_category_text,
                                 reply_markup=BotButtons.ADMIN_INLINE.custom_button(BotTexts, "products_manage").as_markup())
    await state.set_state(adminStates.AdminProductsManage.enter_category_name)


@adminRouter.message(StateFilter(adminStates.AdminProductsManage.enter_category_name))
async def enter_category_name(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    if len(msg.text) <= 64:
        await state.clear()
        await DB.add_category(msg.text)
        await utils.send_admins("category_is_created_alert",
            username=msg.from_user.mention_html(),
            name=msg.text,
        )
        await msg.answer(BotTexts.ADMIN_TEXTS.products_manage_text, 
                                 reply_markup=BotButtons.ADMIN_INLINE.products_manage(BotTexts).as_markup())
    else:
        await msg.reply(BotTexts.ADMIN_TEXTS.name_error)


@adminRouter.callback_query(F.data == "edit_category")
async def edit_category(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    categories = await DB.get_all_categories()
    if categories:
        await call.message.edit_text(BotTexts.ADMIN_TEXTS.select_category, 
                                     reply_markup=BotButtons.ADMIN_INLINE.category_select_menu(BotTexts, categories).as_markup())
        await state.set_state(adminStates.AdminProductsManage.select_category_for_edit)
        
    else:
        await call.answer(BotTexts.ADMIN_TEXTS.no_categories_available)


@adminRouter.callback_query(F.data.startswith("select_category:"), StateFilter(adminStates.AdminProductsManage.select_category_for_edit))
async def select_category_for_edit(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    category = await DB.get_category(cat_id=int(call.data.split(":")[1]))
    await call.message.edit_text(BotTexts.ADMIN_TEXTS.category_text.format(
        name=category.name,
        cat_id=category.cat_id,
    ), reply_markup=BotButtons.ADMIN_INLINE.category_edit(BotTexts, category.cat_id).as_markup())


@adminRouter.callback_query(F.data.startswith("edit_category:"))
async def edit_category_callback(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    data = call.data.split(":")
    category = await DB.get_category(cat_id=int(data[1]))
    if data[2] == "name":
        await call.message.edit_text(BotTexts.ADMIN_TEXTS.enter_new_name_for_category.format(name=category.name),
                                 reply_markup=BotButtons.ADMIN_INLINE.custom_button(BotTexts, "products_manage").as_markup())
        await state.set_state(adminStates.AdminProductsManage.enter_new_name_for_category)
        await state.update_data(category_id=category.cat_id, old_name=category.name)
    elif data[2] == "del":
        await call.message.delete()
        await DB.delete_category(category.cat_id)
        await utils.send_admins("category_is_deleted_alert",
            username=call.from_user.mention_html(),
            name=category.name,
        )
        await call.message.answer(BotTexts.ADMIN_TEXTS.products_manage_text, 
                                 reply_markup=BotButtons.ADMIN_INLINE.products_manage(BotTexts).as_markup())
    else:
        # delete
        await call.message.edit_text(BotTexts.ADMIN_TEXTS.confirm_category_delete.format(name=category.name),
                                     reply_markup=BotButtons.ADMIN_INLINE.confirm(f"edit_category:{category.cat_id}:del", "products_manage").as_markup())



@adminRouter.message(StateFilter(adminStates.AdminProductsManage.enter_new_name_for_category))
async def enter_new_name_for_category(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    if len(msg.text) <= 64:
        data = await state.get_data()
        await state.clear()
        await DB.update_category(category_id=int(data['category_id']), name=msg.text)
        await utils.send_admins("category_is_edited_alert",
            username=msg.from_user.mention_html(),
            old_name=data['old_name'],
            new_name=msg.text,
        )
        await msg.answer(BotTexts.ADMIN_TEXTS.products_manage_text, 
                                 reply_markup=BotButtons.ADMIN_INLINE.products_manage(BotTexts).as_markup())
    else:
        await msg.reply(BotTexts.ADMIN_TEXTS.name_error)

    
@adminRouter.callback_query(F.data == "del_all_categories")
async def del_all_categories(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    await call.message.edit_text(BotTexts.ADMIN_TEXTS.del_all_categories_text,
                                 reply_markup=BotButtons.ADMIN_INLINE.confirm(
                                     f"delete_all_categories", "products_manage"
                                 ).as_markup())
    

@adminRouter.callback_query(F.data == "delete_all_categories")
async def delete_all_categories(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    await call.message.delete()
    await DB.delete_all_categories()
    await utils.send_admins("all_categories_are_deleted_alert",
            username=call.from_user.mention_html(),
        )
    await call.message.answer(BotTexts.ADMIN_TEXTS.products_manage_text, 
                     reply_markup=BotButtons.ADMIN_INLINE.products_manage(BotTexts).as_markup())


### Subcategories
@adminRouter.callback_query(F.data == "add_subcategory")
async def add_cat_opee(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    categories = await DB.get_all_categories()
    if categories:
        await call.message.edit_text(BotTexts.ADMIN_TEXTS.select_category, 
                                  reply_markup=BotButtons.ADMIN_INLINE.category_select_menu(BotTexts, categories).as_markup())
        await state.set_state(adminStates.AdminProductsManage.select_category_for_add_sub)
    else:
        await call.answer(BotTexts.ADMIN_TEXTS.no_categories_available)


@adminRouter.callback_query(F.data.startswith("select_category"), StateFilter(adminStates.AdminProductsManage.select_category_for_add_sub))
async def select_category_for_add_sub(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    category = await DB.get_category(cat_id=int(call.data.split(":")[1]))
    await call.message.edit_text(BotTexts.ADMIN_TEXTS.enter_name_for_subcategory,
                                 reply_markup=BotButtons.ADMIN_INLINE.custom_button(BotTexts, "products_manage").as_markup())
    await state.set_state(adminStates.AdminProductsManage.enter_subcategory_name)
    await state.update_data(category=category)


@adminRouter.message(StateFilter(adminStates.AdminProductsManage.enter_subcategory_name))
async def enter_subcategory_name(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    if len(msg.text) <= 64:
        category: models.Category = (await state.get_data())['category']
        await state.clear()
        await DB.add_subcategory(msg.text, category.cat_id)
        await utils.send_admins("subcategory_is_created_alert",
            username=msg.from_user.mention_html(),
            name=msg.text,
            cat_name=category.name,
        )
        await msg.answer(BotTexts.ADMIN_TEXTS.products_manage_text, 
                                 reply_markup=BotButtons.ADMIN_INLINE.products_manage(BotTexts).as_markup())
    else:
        await msg.reply(BotTexts.ADMIN_TEXTS.name_error)


@adminRouter.callback_query(F.data == "edit_subcategory")
async def edit_subcategory(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    categories = await DB.get_all_categories()
    if categories:
        if await DB.get_all_subcategories():
            await call.message.edit_text(BotTexts.ADMIN_TEXTS.select_category, 
                                  reply_markup=BotButtons.ADMIN_INLINE.category_select_menu(BotTexts, categories).as_markup())
            await state.set_state(adminStates.AdminProductsManage.select_category_for_edit_sub)
        else:
            await call.answer(BotTexts.ADMIN_TEXTS.no_subcategories_available)
    else:
        await call.answer(BotTexts.ADMIN_TEXTS.no_categories_available)


@adminRouter.callback_query(F.data.startswith("select_category:"), StateFilter(adminStates.AdminProductsManage.select_category_for_edit_sub))
async def select_category_for_edit_sub(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    subcategories = await DB.get_subcategories(cat_id=int(call.data.split(":")[1]))
    if subcategories:
        await state.clear()
        await call.message.edit_text(BotTexts.ADMIN_TEXTS.select_subcategory,
                                     reply_markup=BotButtons.ADMIN_INLINE.subcategory_select_menu(BotTexts, subcategories).as_markup())
        await state.set_state(adminStates.AdminProductsManage.select_sub_for_edit)
        await state.update_data(category_id=int(call.data.split(":")[1]))
    else:
        await call.answer(BotTexts.ADMIN_TEXTS.no_subcategories_available_in_this_category)
    

@adminRouter.callback_query(F.data.startswith("select_subcategory:"), StateFilter(adminStates.AdminProductsManage.select_sub_for_edit))
async def select_sub_for_edit(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    category = await DB.get_category(cat_id=int((await state.get_data())['category_id']))
    await state.clear()
    subcategory = await DB.get_subcategory(sub_cat_id=int(call.data.split(":")[1]))
    await call.message.edit_text(BotTexts.ADMIN_TEXTS.subcategory_text.format(
        name=subcategory.name,
        sub_cat_id=subcategory.sub_cat_id,
        cat_name=category.name,
        cat_id=category.cat_id,
    ), reply_markup=BotButtons.ADMIN_INLINE.category_edit(BotTexts, subcategory.sub_cat_id, True).as_markup())


@adminRouter.callback_query(F.data.startswith("edit_subcategory:"))
async def edit_subcategory(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    data = call.data.split(":")
    subcategory = await DB.get_subcategory(sub_cat_id=int(data[1]))
    if data[2] == "name":
        await call.message.edit_text(BotTexts.ADMIN_TEXTS.enter_new_name_for_subcategory.format(name=subcategory.name),
                                 reply_markup=BotButtons.ADMIN_INLINE.custom_button(BotTexts, "products_manage").as_markup())
        await state.set_state(adminStates.AdminProductsManage.enter_new_name_for_sub)
        await state.update_data(subcategory_id=subcategory.sub_cat_id, old_name=subcategory.name)
    elif data[2] == "del":
        await call.message.delete()
        await DB.delete_subcategory(subcategory.sub_cat_id)
        await utils.send_admins("subcategory_is_deleted_alert",
            username=call.from_user.mention_html(),
            name=subcategory.name,
        )
        await call.message.answer(BotTexts.ADMIN_TEXTS.products_manage_text, 
                                 reply_markup=BotButtons.ADMIN_INLINE.products_manage(BotTexts).as_markup())
    elif data[2] == "move":
        categories = await DB.get_all_categories()
        await call.message.edit_text(BotTexts.ADMIN_TEXTS.select_category,
                                     reply_markup=BotButtons.ADMIN_INLINE.category_select_menu(BotTexts, categories).as_markup())
        await state.set_state(adminStates.AdminProductsManage.select_category_for_move_sub)
        await state.update_data(subcategory=subcategory)
    else:
        # delete
        await call.message.edit_text(BotTexts.ADMIN_TEXTS.confirm_subcategory_delete.format(name=subcategory.name),
                                     reply_markup=BotButtons.ADMIN_INLINE.confirm(f"edit_subcategory:{subcategory.sub_cat_id}:del", "products_manage").as_markup())


@adminRouter.callback_query(F.data.startswith("select_category:"), StateFilter(adminStates.AdminProductsManage.select_category_for_move_sub))
async def select_category_for_move_sub(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    subcategory: models.SubCategory = (await state.get_data())['subcategory']
    await state.clear()
    category = await DB.get_category(cat_id=subcategory.cat_id)
    await DB.update_subcategory(subcategory_id=subcategory.sub_cat_id, cat_id=int(call.data.split(":")[1]))
    new_category = await DB.get_category(cat_id=int(call.data.split(":")[1]))
    await call.message.delete()
    await utils.send_admins("subcategory_has_been_moved_deleted_alert",
        username=call.from_user.mention_html(),
        sub_name=subcategory.name,
        old_cat_name=category.name,
        new_cat_name=new_category.name
    )
    await call.message.answer(BotTexts.ADMIN_TEXTS.subcategory_text.format(
        name=subcategory.name,
        sub_cat_id=subcategory.sub_cat_id,
        cat_name=new_category.name,
        cat_id=new_category.cat_id,
    ), reply_markup=BotButtons.ADMIN_INLINE.category_edit(BotTexts, subcategory.sub_cat_id, True).as_markup())



@adminRouter.message(StateFilter(adminStates.AdminProductsManage.enter_new_name_for_sub))
async def enter_new_name_for_sub(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    if len(msg.text) <= 64:
        data = await state.get_data()
        await state.clear()
        await DB.update_subcategory(subcategory_id=int(data['subcategory_id']), name=msg.text)
        await utils.send_admins("subcategory_is_edited_alert",
            username=msg.from_user.mention_html(),
            old_name=data['old_name'],
            new_name=msg.text,
        )
        await msg.answer(BotTexts.ADMIN_TEXTS.products_manage_text, 
                                 reply_markup=BotButtons.ADMIN_INLINE.products_manage(BotTexts).as_markup())
    else:
        await msg.reply(BotTexts.ADMIN_TEXTS.name_error)

    
@adminRouter.callback_query(F.data == "del_all_subcategories")
async def del_all_subcategories(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    await call.message.edit_text(BotTexts.ADMIN_TEXTS.del_all_subcategories_text,
                                 reply_markup=BotButtons.ADMIN_INLINE.confirm(
                                     f"delete_all_subcategories", "products_manage"
                                 ).as_markup())
    

@adminRouter.callback_query(F.data == "delete_all_subcategories")
async def delete_all_subcategories(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    await call.message.delete()
    await DB.delete_all_subcategories()
    await utils.send_admins("all_subcategories_are_deleted_alert",
        username=call.from_user.mention_html(),
    )
    await call.message.answer(BotTexts.ADMIN_TEXTS.products_manage_text, 
                     reply_markup=BotButtons.ADMIN_INLINE.products_manage(BotTexts).as_markup())
    

### Positions
@adminRouter.callback_query(F.data == "add_position")
async def add_position(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    categories = await DB.get_all_categories()
    if categories:
        await call.message.edit_text(BotTexts.ADMIN_TEXTS.select_category,
                                     reply_markup=BotButtons.ADMIN_INLINE.category_select_menu(BotTexts, categories).as_markup())
        await state.set_state(adminStates.AdminProductsManage.select_category_for_add_position)
    else:
        await call.answer(BotTexts.ADMIN_TEXTS.no_categories_available)


@adminRouter.callback_query(F.data.startswith("select_category:"), StateFilter(adminStates.AdminProductsManage.select_category_for_add_position, adminStates.AdminProductsManage.select_subcategory_for_add_position))
async def select_category_for_add_position(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    data = call.data.split(":")
    subcategories = await DB.get_subcategories(cat_id=int(data[1]))
    if subcategories and len(data) == 2:
        await call.message.edit_text(BotTexts.ADMIN_TEXTS.select_subcategory, 
                                    reply_markup=BotButtons.ADMIN_INLINE.subcategory_select_menu(BotTexts, subcategories, True).as_markup())
        await state.set_state(adminStates.AdminProductsManage.select_subcategory_for_add_position)
    else:
        await state.set_state(adminStates.AdminProductsManage.enter_position_name)
        await call.message.edit_text(BotTexts.ADMIN_TEXTS.enter_position_name,
                                     reply_markup=BotButtons.ADMIN_INLINE.custom_button(BotTexts, "products_manage").as_markup())
    await state.update_data(category_id=data[1])
        
        
@adminRouter.callback_query(F.data.startswith("select_subcategory:"), StateFilter(adminStates.AdminProductsManage.select_subcategory_for_add_position))
async def select_subcategory_for_add_position(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.set_state(adminStates.AdminProductsManage.enter_position_name)
    await state.update_data(subcategory_id=call.data.split(":")[1])
    await call.message.edit_text(BotTexts.ADMIN_TEXTS.enter_position_name,
                                 reply_markup=BotButtons.ADMIN_INLINE.custom_button(BotTexts, "products_manage").as_markup())
    

@adminRouter.message(StateFilter(adminStates.AdminProductsManage.enter_position_name))
async def enter_position_name(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    if len(msg.text) <= 64:
        await state.set_state(adminStates.AdminProductsManage.enter_position_price)
        await state.update_data(name=msg.text)
        await msg.reply(BotTexts.ADMIN_TEXTS.enter_position_price,
                                 reply_markup=BotButtons.ADMIN_INLINE.custom_button(BotTexts, "products_manage").as_markup())
    else:
        await msg.reply(BotTexts.ADMIN_TEXTS.name_error)


@adminRouter.message(StateFilter(adminStates.AdminProductsManage.enter_position_price))
async def enter_position_price(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    if msg.text.isdigit() or msg.text.replace(".", "").replace(",", "").isdigit():
        await state.set_state(adminStates.AdminProductsManage.enter_position_description)
        await state.update_data(price=msg.text)
        await msg.reply(BotTexts.ADMIN_TEXTS.enter_position_description,
                                 reply_markup=BotButtons.ADMIN_INLINE.custom_button(BotTexts, "products_manage").as_markup())
    else:
        await msg.reply(BotTexts.ADMIN_TEXTS.value_is_no_number)


@adminRouter.message(StateFilter(adminStates.AdminProductsManage.enter_position_description))
async def enter_position_description(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    if len(msg.text) <= 2000:
        await state.update_data(description=None if msg.text == "-" else msg.html_text)
        # Ask for position type - using reply keyboard
        from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="💎 Бесконечный")], [KeyboardButton(text="📦 С количеством")]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await msg.reply("<b>❓ Выберите тип товара:</b>\n\n💎 Бесконечный - товар всегда в наличии\n📦 С количеством - ограниченное количество", reply_markup=kb)
        await state.set_state(adminStates.AdminProductsManage.enter_position_type)
    else:
        await msg.reply(BotTexts.ADMIN_TEXTS.description_error)


@adminRouter.message(StateFilter(adminStates.AdminProductsManage.enter_position_type))
async def enter_position_type(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    if msg.text == "💎 Бесконечный":
        await state.update_data(is_infinity=True, quantity=None)
        await msg.reply(BotTexts.ADMIN_TEXTS.enter_position_photo, 
                    reply_markup=BotButtons.ADMIN_INLINE.custom_button(BotTexts, "products_manage").as_markup())
        await state.set_state(adminStates.AdminProductsManage.enter_position_photo)
    elif msg.text == "📦 С количеством":
        await state.update_data(is_infinity=False)
        await msg.reply("<b>❗ Введите количество товара:</b>", 
                    reply_markup=BotButtons.ADMIN_INLINE.custom_button(BotTexts, "products_manage").as_markup())
        await state.set_state(adminStates.AdminProductsManage.enter_position_quantity)
    else:
        await msg.reply("❌ Пожалуйста выберите один из вариантов выше")


@adminRouter.message(StateFilter(adminStates.AdminProductsManage.enter_position_quantity))
async def enter_position_quantity(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    if msg.text.isdigit():
        await state.update_data(quantity=int(msg.text))
        await msg.reply(BotTexts.ADMIN_TEXTS.enter_position_photo, 
                    reply_markup=BotButtons.ADMIN_INLINE.custom_button(BotTexts, "products_manage").as_markup())
        await state.set_state(adminStates.AdminProductsManage.enter_position_photo)
    else:
        await msg.reply(BotTexts.ADMIN_TEXTS.value_is_no_number)


@adminRouter.message(StateFilter(adminStates.AdminProductsManage.enter_position_photo), F.photo)
@adminRouter.message(StateFilter(adminStates.AdminProductsManage.enter_position_photo), F.text == "-")
async def enter_position_photo(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    data = await state.get_data()
    await state.clear()
    
    currency = (await DB.get_settings()).currency.value
    if currency == "uzs":
        price_uzs = float(data['price'])
        price_eur = await utils.get_exchange(price_uzs, 'UZS', 'EUR')
        price_usd = await utils.get_exchange(price_uzs, 'UZS', 'USD')
    elif currency == 'usd':
        price_usd = float(data['price'])
        price_uzs = await utils.get_exchange(price_usd, 'USD', 'UZS')
        price_eur = await utils.get_exchange(price_usd, 'USD', 'EUR')
    else:
        # eur
        price_eur = float(data['price'])
        price_usd = await utils.get_exchange(price_eur, 'EUR', 'USD')
        price_uzs = await utils.get_exchange(price_eur, 'EUR', 'UZS')

    photo_id = None if msg.text == "-" else msg.photo[-1].file_id
    is_infinity = data.get('is_infinity', True)
    quantity = data.get('quantity')
    
    await DB.add_position(
        data['name'],
        price_uzs,
        price_usd,
        price_eur,
        data['description'],
        photo_id,
        data.get("category_id"),
        data.get("subcategory_id"),
        is_infinity,
        True,  # item_type
    )
    
    # If not infinite, add quantity to position
    if not is_infinity and quantity:
        position = await DB.get_position(name=data['name'])
        if position:
            # Create items for this position with the specified quantity
            for i in range(quantity):
                await DB.add_item(f"item_{i}", position.pos_id, int(data.get("category_id")))
    category = await DB.get_category(cat_id=int(data.get("category_id")))
    subcategory = await DB.get_subcategory(sub_cat_id=int(data.get("subcategory_id"))) if data.get("subcategory_id") else None
    await utils.send_admins("position_is_created_alert",
        username=msg.from_user.mention_html(),
        cat_name=category.name,
        cat_id=category.cat_id,
        subcategory=f"<code>{subcategory.name}</code> [<code>{subcategory.sub_cat_id}</code>]" if subcategory else None,
        name=data['name'],
        price=data['price'],
        curr=BotConfig.CURRENCIES[currency]['sign'],
        position_type="Товар",
        item_type="Разовая",
        description=data['description'],
        photo=photo_id)


@adminRouter.callback_query(F.data == "edit_position")
async def edit_position(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    if await DB.get_all_positions():
        categories = await DB.get_all_categories()
        if categories:
            try:
                await call.message.edit_text(BotTexts.ADMIN_TEXTS.select_category, 
                                  reply_markup=BotButtons.ADMIN_INLINE.category_select_menu(BotTexts, categories).as_markup())
            except:
                try:
                    await call.message.delete()
                except:
                    pass
                await call.message.answer(BotTexts.ADMIN_TEXTS.select_category, 
                                  reply_markup=BotButtons.ADMIN_INLINE.category_select_menu(BotTexts, categories).as_markup())
            await state.set_state(adminStates.AdminProductsManage.select_category_for_edit_position)
        else:
            await call.answer(BotTexts.ADMIN_TEXTS.no_categories_available)
    else:
        await call.answer(BotTexts.ADMIN_TEXTS.no_positions_available)


@adminRouter.callback_query(F.data.startswith("select_category:"), StateFilter(adminStates.AdminProductsManage.select_category_for_edit_position))
async def select_category_for_edit_position(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    positions = await DB.get_positions(cat_id=int(call.data.split(":")[1]), sub_cat_id=None)
    sub_categories = await DB.get_subcategories(cat_id=int(call.data.split(":")[1]))
    if sub_categories:
        await call.message.edit_text(
            BotTexts.ADMIN_TEXTS.select_subcategory,
            reply_markup=BotButtons.ADMIN_INLINE.subcategory_select_menu(BotTexts, subcategories=sub_categories, 
                                                                         positions=positions, is_for_edit_position=True).as_markup()
        )
        await state.set_state(adminStates.AdminProductsManage.select_subcategory_for_edit_position)
    else:
        if positions:
            await call.message.edit_text(
                BotTexts.ADMIN_TEXTS.select_position,
                reply_markup=BotButtons.ADMIN_INLINE.position_select_menu(BotTexts, positions).as_markup(),
            )
            await state.set_state(adminStates.AdminProductsManage.select_position_for_edit)
        else:
            await call.answer(BotTexts.ADMIN_TEXTS.no_positions_available_in_this_category)


@adminRouter.callback_query(F.data.startswith("select_subcategory:"), StateFilter(adminStates.AdminProductsManage.select_subcategory_for_edit_position))
async def select_subcategory_for_edit_position(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    positions = await DB.get_positions(sub_cat_id=int(call.data.split(":")[1]))
    if positions:
        await call.message.edit_text(
            BotTexts.ADMIN_TEXTS.select_position,
            reply_markup=BotButtons.ADMIN_INLINE.position_select_menu(BotTexts, positions).as_markup(),
        )
        await state.set_state(adminStates.AdminProductsManage.select_position_for_edit)
    else:
        await call.answer(BotTexts.ADMIN_TEXTS.no_positions_available_in_this_subcategory)


async def get_position_info(BotTexts, position, message, is_edit=True):
    category = await DB.get_category(cat_id=position.cat_id)
    subcategory = await DB.get_subcategory(sub_cat_id=position.sub_cat_id)
    items_count = len(await DB.get_items(pos_id=position.pos_id))
    currency = (await DB.get_settings()).currency.value
    if currency == "rub":
        price = position.price_uzs
    elif currency == 'usd':
        price = position.price_usd
    else:
        # eur
        price = position.price_eur
    
    # Handle item_type safely
    item_type = position.item_type
    if isinstance(item_type, bool) or item_type is True or item_type == True:
        item_type_str = "Бесконечный"
    elif item_type == "text" or item_type in ["text", "1", True]:
        item_type_str = "Текст"
    elif item_type == "file":
        item_type_str = "Файл"
    else:
        item_type_str = str(item_type)
    
    text = BotTexts.ADMIN_TEXTS.position_text.format(
            pos_name=position.name,
            cat_name=category.name,
            cat_id=category.cat_id,
            subcategory=f"<code>{subcategory.name}</code> [<code>{subcategory.sub_cat_id}</code>]" if subcategory else None,
            price=price,
            curr=BotConfig.CURRENCIES[currency]['sign'],
            position_type=BotTexts.ADMIN_TEXTS.position_type[position.is_infinity],
            item_type=item_type_str,
            description=position.description,
            items_count=items_count,
        )
    if position.photo and position.photo != "-":
        try:
            await message.delete()
        except TelegramBadRequest:
            pass
        await message.answer_photo(caption=text, photo=position.photo,
        reply_markup=BotButtons.ADMIN_INLINE.position_edit(BotTexts, position.pos_id).as_markup())
    else:
        if is_edit:
            await message.edit_text(text=text,
                                    reply_markup=BotButtons.ADMIN_INLINE.position_edit(BotTexts, position.pos_id).as_markup())
        else:
            await message.answer(text=text,
                                    reply_markup=BotButtons.ADMIN_INLINE.position_edit(BotTexts, position.pos_id).as_markup())


@adminRouter.callback_query(F.data.startswith("select_position:"), StateFilter(adminStates.AdminProductsManage.select_position_for_edit, adminStates.AdminProductsManage.select_subcategory_for_edit_position))
async def select_position_for_edit(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    position = await DB.get_position(pos_id=int(call.data.split(":")[1]))
    await get_position_info(BotTexts, position, call.message)


@adminRouter.callback_query(F.data.startswith("position_edit:"))
async def position_edit(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    data = call.data.split(":")
    position = await DB.get_position(pos_id=int(data[1]))
    await call.message.delete()
    if data[2] == "price":
        await call.message.answer(BotTexts.ADMIN_TEXTS.enter_new_position_price)
        await state.set_state(adminStates.AdminProductsManage.enter_new_position_price)
        await state.update_data(position_id=position.pos_id)
    elif data[2] == "name":
        await call.message.answer(BotTexts.ADMIN_TEXTS.enter_new_position_name)
        await state.set_state(adminStates.AdminProductsManage.enter_new_position_name)
        await state.update_data(position_id=position.pos_id)
    elif data[2] == "description":
        await call.message.answer(BotTexts.ADMIN_TEXTS.enter_new_position_description)
        await state.set_state(adminStates.AdminProductsManage.enter_new_position_description)
        await state.update_data(position_id=position.pos_id)
    elif data[2] == "photo":
        await call.message.answer(BotTexts.ADMIN_TEXTS.enter_new_position_photo)
        await state.set_state(adminStates.AdminProductsManage.enter_new_position_photo)
        await state.update_data(position_id=position.pos_id)
    elif data[2] == "position_type":
        await call.message.answer(BotTexts.ADMIN_TEXTS.enter_position_type)
        await state.set_state(adminStates.AdminProductsManage.enter_new_position_type)
        await state.update_data(position_id=position.pos_id)
    elif data[2] == "delete":
        await call.message.answer(BotTexts.ADMIN_TEXTS.confirm_position_delete.format(name=position.name),
                                     reply_markup=BotButtons.ADMIN_INLINE.confirm(f"position_edit:{position.pos_id}:del", "products_manage").as_markup())
    elif data[2] == "del":
        await DB.delete_position(position.pos_id)
        await utils.send_admins("position_is_deleted_alert",
            username=call.from_user.mention_html(),
            name=position.name,
        )
        await call.message.answer(BotTexts.ADMIN_TEXTS.products_manage_text, 
                                  reply_markup=BotButtons.ADMIN_INLINE.products_manage(BotTexts).as_markup())
    elif data[2] == "move":
        categories = await DB.get_all_categories()
        await call.message.answer(BotTexts.ADMIN_TEXTS.select_category,
                                  reply_markup=BotButtons.ADMIN_INLINE.category_select_menu(BotTexts, categories).as_markup())
        await state.set_state(adminStates.AdminProductsManage.select_category_for_move_position)
        await state.update_data(position_id=position.pos_id)
    elif data[2] == "clear_items":
        await call.message.answer(BotTexts.ADMIN_TEXTS.confirm_position_items_delete.format(name=position.name),
                                  reply_markup=BotButtons.ADMIN_INLINE.confirm(f"position_edit:{position.pos_id}:confirm_delete_items", "products_manage").as_markup())
    elif data[2] == "upload_items":
        await call.message.answer(BotTexts.ADMIN_TEXTS.enter_data_items["text_infinity" if position.item_type == "text" and position.is_infinity else position.item_type],
                                     reply_markup=BotButtons.ADMIN_INLINE.custom_button(BotTexts, "products_manage").as_markup())
        await state.set_state(adminStates.AdminProductsManage.enter_data_items)
        await state.update_data(position=position, count_add_items=0)
    elif data[2] == "get_items":
        try:
            items = await DB.get_items(pos_id=position.pos_id)
            text = ""
            for item in items:
                text += f"{BotTexts.ADMIN_TEXTS.item} #{item.item_id}:"
                if item.data:
                    text += f"\n{item.data}"
                if item.file_id:
                    text += f"\n{item.file_id}"
                text += "\n\n"
            with open(f"position_items_{position.pos_id}.txt", "w", encoding="utf-8") as file:
                file.write(f"{BotTexts.ADMIN_TEXTS.position}: {position.name} | #{position.pos_id}: \n\n{text}")
                file.close()

            await call.message.answer_document(document=FSInputFile(f"position_items_{position.pos_id}.txt"), 
                                            caption=BotTexts.ADMIN_TEXTS.list_of_items.format(name=position.name))
            os.remove(f"position_items_{position.pos_id}.txt")
        except:
            print_exc()
            await call.message.answer(BotTexts.ADMIN_TEXTS.get_list_of_items_error,
                                      reply_markup=BotButtons.ADMIN_INLINE.custom_button(BotTexts, "products_manage").as_markup())
    elif data[2] == "quantity":
        # Show quantity management options
        items_count = await DB.get_items_count_by_position(position.pos_id)
        text = f"<b>📊 Управление количеством товара</b>\n\n"
        text += f"<b>Товар:</b> {position.name}\n"
        text += f"<b>Текущее количество:</b> {items_count}\n\n"
        text += f"Выберите действие:"
        
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="➕ Добавить", callback_data=f"position_quantity:add:{position.pos_id}"),
                 InlineKeyboardButton(text="➖ Уменьшить", callback_data=f"position_quantity:remove:{position.pos_id}")],
                [InlineKeyboardButton(text="🔄 Установить", callback_data=f"position_quantity:set:{position.pos_id}"),
                 InlineKeyboardButton(text="🗑️ Удалить всё", callback_data=f"position_quantity:clear:{position.pos_id}")],
                [InlineKeyboardButton(text="<< Назад", callback_data=f"position_quantity:back:{position.pos_id}")]
            ]
        )
        try:
            await call.message.delete()
        except:
            pass
        await call.message.answer(text, reply_markup=keyboard)
    else:
        # confirm_delete_items (for "confirm_delete_items" callback)
        await DB.delete_position_items(position.pos_id)
        await utils.send_admins("position_items_is_deleted_alert",
            username=call.from_user.mention_html(),
            name=position.name,
        )
        await get_position_info(BotTexts, await DB.get_position(pos_id=position.pos_id), call.message, False)


@adminRouter.callback_query(F.data.startswith("position_quantity:"))
async def position_quantity(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    data = call.data.split(":")
    action = data[1]
    position_id = int(data[2])
    
    if action == "add":
        try:
            await call.message.delete()
        except:
            pass
        await call.message.answer("<b>❗ Введите количество товара для добавления:</b>",
                                    reply_markup=BotButtons.ADMIN_INLINE.custom_button(BotTexts, "products_manage").as_markup())
        await state.set_state(adminStates.AdminProductsManage.enter_position_quantity_change)
        await state.update_data(position_id=position_id, action="add")
    elif action == "remove":
        try:
            await call.message.delete()
        except:
            pass
        await call.message.answer("<b>❗ Введите количество товара для удаления:</b>",
                                    reply_markup=BotButtons.ADMIN_INLINE.custom_button(BotTexts, "products_manage").as_markup())
        await state.set_state(adminStates.AdminProductsManage.enter_position_quantity_change)
        await state.update_data(position_id=position_id, action="remove")
    elif action == "set":
        try:
            await call.message.delete()
        except:
            pass
        await call.message.answer("<b>❗ Введите новое количество товара:</b>",
                                    reply_markup=BotButtons.ADMIN_INLINE.custom_button(BotTexts, "products_manage").as_markup())
        await state.set_state(adminStates.AdminProductsManage.enter_position_quantity_change)
        await state.update_data(position_id=position_id, action="set")
    elif action == "clear":
        await DB.delete_all_items_by_position(position_id)
        position = await DB.get_position(pos_id=position_id)
        try:
            await call.message.delete()
        except:
            pass
        await utils.send_admins("quantity_items_cleared",
            username=call.from_user.mention_html(),
            name=position.name,
        )
        await get_position_info(BotTexts, position, call.message, False)
    elif action == "back":
        position = await DB.get_position(pos_id=position_id)
        await state.clear()
        try:
            await call.message.delete()
        except:
            pass
        await get_position_info(BotTexts, position, call.message, False)


@adminRouter.message(StateFilter(adminStates.AdminProductsManage.enter_position_quantity_change))
async def enter_position_quantity_change(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    if msg.text.isdigit():
        data = await state.get_data()
        await state.clear()
        
        position_id = data['position_id']
        action = data['action']
        quantity = int(msg.text)
        position = await DB.get_position(pos_id=position_id)
        
        if action == "add":
            for i in range(quantity):
                await DB.add_item(f"item_{i}", position_id, position.cat_id)
            await utils.send_admins("quantity_items_added",
                username=msg.from_user.mention_html(),
                name=position.name,
                quantity=quantity,
            )
        elif action == "remove":
            items = await DB.get_items(pos_id=position_id)
            for i in range(min(quantity, len(items))):
                await DB.delete_item(items[i].item_id)
            await utils.send_admins("quantity_items_removed",
                username=msg.from_user.mention_html(),
                name=position.name,
                quantity=min(quantity, len(items)),
            )
        elif action == "set":
            current_items = await DB.get_items(pos_id=position_id)
            current_count = len(current_items)
            
            if quantity > current_count:
                for i in range(quantity - current_count):
                    await DB.add_item(f"item_{i}", position_id, position.cat_id)
            elif quantity < current_count:
                for i in range(current_count - quantity):
                    await DB.delete_item(current_items[i].item_id)
            
            await utils.send_admins("quantity_items_set",
                username=msg.from_user.mention_html(),
                name=position.name,
                quantity=quantity,
            )
        
        await get_position_info(BotTexts, await DB.get_position(pos_id=position_id), msg, False)
    else:
        await msg.reply(BotTexts.ADMIN_TEXTS.value_is_no_number)


@adminRouter.message(StateFilter(adminStates.AdminProductsManage.enter_new_position_price))
async def enter_new_position_price(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    if msg.text.isdigit() or msg.text.replace(",", "").replace(".", "").isdigit():
        position_id = (await state.get_data()).get('position_id')
        await state.clear()
        position = await DB.get_position(pos_id=position_id)
        currency = (await DB.get_settings()).currency.value
        if currency == "rub":
            price_uzs = float(msg.text)
            price_eur = await utils.get_exchange(price_uzs, 'rub', 'EUR')
            price_usd = await utils.get_exchange(price_uzs, 'rub', 'USD')
        elif currency == 'usd':
            price_usd = float(msg.text)
            price_uzs = await utils.get_exchange(price_usd, 'USD', 'rub')
            price_eur = await utils.get_exchange(price_usd, 'USD', 'EUR')
        else:
            # eur
            price_eur = float(msg.text)
            price_usd = await utils.get_exchange(price_eur, 'EUR', 'USD')
            price_uzs = await utils.get_exchange(price_eur, 'EUR', 'rub')
        await DB.update_position(position_id=position.pos_id, price_uzs=price_uzs, price_usd=price_usd, price_eur=price_eur)
        await get_position_info(BotTexts, await DB.get_position(pos_id=position.pos_id), msg, False)
    else:
        await msg.reply(BotTexts.ADMIN_TEXTS.value_is_no_number)
    

@adminRouter.message(StateFilter(adminStates.AdminProductsManage.enter_new_position_name))
async def enter_new_position_name(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    if len(msg.text) <= 64:
        position_id = (await state.get_data()).get('position_id')
        await state.clear()
        position = await DB.get_position(pos_id=position_id)
        await DB.update_position(position_id=position.pos_id, name=msg.text)
        await get_position_info(BotTexts, await DB.get_position(pos_id=position.pos_id), msg, False)
    else:
        await msg.reply(BotTexts.ADMIN_TEXTS.name_error)


@adminRouter.message(StateFilter(adminStates.AdminProductsManage.enter_new_position_description))
async def enter_new_position_description(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    if len(msg.text) <= 2000:
        position_id = (await state.get_data()).get('position_id')
        await state.clear()
        position = await DB.get_position(pos_id=position_id)
        await DB.update_position(position_id=position.pos_id, description=None if msg.text == "-" else msg.html_text)
        await get_position_info(BotTexts, await DB.get_position(pos_id=position.pos_id), msg, False)
    else:
        await msg.reply(BotTexts.ADMIN_TEXTS.description_error)


@adminRouter.message(StateFilter(adminStates.AdminProductsManage.enter_new_position_photo), F.photo)
@adminRouter.message(StateFilter(adminStates.AdminProductsManage.enter_new_position_photo), F.text == "-")
async def enter_new_position_photo(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    data = await state.get_data()
    position = data.get('position')
    
    if not position:
        position_id = data.get('position_id')
        if position_id:
            position = await DB.get_position(pos_id=position_id)
    
    await state.clear()
    
    if position:
        await DB.update_position(position_id=position.pos_id, photo=None if msg.text == "-" else msg.photo[-1].file_id)
        await get_position_info(BotTexts, await DB.get_position(pos_id=position.pos_id), msg, False)
    else:
        await msg.reply("❌ Ошибка: позиция не найдена")


@adminRouter.message(StateFilter(adminStates.AdminProductsManage.enter_new_position_type), F.text.in_({"+", "-"}))
async def enter_new_position_type(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    position_id = (await state.get_data()).get('position_id')
    await state.clear()
    position = await DB.get_position(pos_id=position_id)
    await DB.update_position(position_id=position.pos_id, is_infinity=True if msg.text == "+" else False)
    await get_position_info(BotTexts, await DB.get_position(pos_id=position.pos_id), msg, False)


@adminRouter.callback_query(F.data.startswith("select_category:"), StateFilter(adminStates.AdminProductsManage.select_category_for_move_position, adminStates.AdminProductsManage.select_subcategory_for_move_position))
async def select_category_for_move_position(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    position_id = (await state.get_data()).get('position_id')
    position = await DB.get_position(pos_id=position_id)
    data = call.data.split(":")
    subcategories = await DB.get_subcategories(cat_id=int(data[1]))
    if subcategories and len(data) == 2:
        await call.message.edit_text(BotTexts.ADMIN_TEXTS.select_subcategory, 
                                    reply_markup=BotButtons.ADMIN_INLINE.subcategory_select_menu(BotTexts, subcategories, True).as_markup())
        await state.set_state(adminStates.AdminProductsManage.select_subcategory_for_move_position)
    else: 
        await DB.update_position(position_id=position.pos_id, cat_id=int(data[1]))
        await get_position_info(BotTexts, await DB.get_position(pos_id=position.pos_id), call.message)
        
        
@adminRouter.callback_query(F.data.startswith("select_subcategory:"), StateFilter(adminStates.AdminProductsManage.select_subcategory_for_move_position))
async def select_subcategory_for_move_position(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    position_id = (await state.get_data()).get('position_id')
    position = await DB.get_position(pos_id=position_id)
    subcategory = await DB.get_subcategory(sub_cat_id=int(call.data.split(":")[1]))
    await DB.update_position(position_id=position.pos_id, cat_id=subcategory.cat_id, sub_cat_id=subcategory.sub_cat_id)
    await get_position_info(BotTexts, await DB.get_position(pos_id=position.pos_id), call.message)


@adminRouter.callback_query(F.data == "del_all_positions")
async def del_all_positions(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    await call.message.edit_text(BotTexts.ADMIN_TEXTS.del_all_positions_text,
                                 reply_markup=BotButtons.ADMIN_INLINE.confirm(
                                     f"delete_all_positions", "products_manage"
                                 ).as_markup())
    

@adminRouter.callback_query(F.data == "delete_all_positions")
async def delete_all_positions(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    await call.message.delete()
    await DB.delete_all_positions()
    await utils.send_admins("all_positions_are_deleted_alert",
            username=call.from_user.mention_html(),
        )
    await call.message.answer(BotTexts.ADMIN_TEXTS.products_manage_text, 
                     reply_markup=BotButtons.ADMIN_INLINE.products_manage(BotTexts).as_markup())


### Items
@adminRouter.message(StateFilter(adminStates.AdminProductsManage.enter_data_items), F.photo, F.document)
@adminRouter.message(StateFilter(adminStates.AdminProductsManage.enter_data_items))
async def enter_data_items(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    cache_message = await msg.reply(BotTexts.ADMIN_TEXTS.products_add_wait)
    try:
        count_add, new_count = 0, 0
        data = await state.get_data()
        position: models.Position = data['position']
        if position.item_type == "text":
            if position.is_infinity:
                items = msg.text
                new_count = data["count_add_items"] + 1
            else:
                if msg.document:
                    file = await msg.bot.get_file(msg.document.file_id)
                    await msg.bot.download_file(file.file_path,
                                                destination=msg.document.file_name)
                    with open(msg.document.file_name, 'r', encoding="utf-8") as f:
                        items = f.read().split("\n\n")
                        f.close()
                    os.remove(msg.document.file_name)
                else:                    
                    items = msg.text.split("\n\n")
                
                for check_item in items:
                    if not check_item.isspace() and check_item != "": count_add += 1
                new_count = data["count_add_items"] + count_add
            await DB.add_items(position.cat_id, position.pos_id, items, None, False, position.is_infinity)
        elif position.item_type == "photo" and msg.content_type == "photo":
            await DB.add_items(position.cat_id, position.pos_id, None if not msg.html_text else msg.html_text, f"photo:{msg.photo[-1].file_id}", True)
            new_count = data["count_add_items"] + 1
        elif position.item_type == "file" and msg.content_type == "document":
            await DB.add_items(position.cat_id, position.pos_id, None if not msg.html_text else msg.html_text, f"file:{msg.document.file_id}", True)
            new_count = data["count_add_items"] + 1
        else:
            return await msg.reply(BotTexts.ADMIN_TEXTS.no_need_item_type_sent)
        await state.update_data(count_add_items=new_count)
        await cache_message.edit_text(BotTexts.ADMIN_TEXTS.products_successful_added.format(count=count_add or 1),
                                    reply_markup=BotButtons.ADMIN_INLINE.custom_button(BotTexts, "stop_upload_items", 
                                                                                        BotTexts.ADMIN_TEXTS.stop_upload_items).as_markup() if not position.is_infinity else None)
    except:
        print_exc()
        await cache_message.edit_text(BotTexts.ADMIN_TEXTS.upload_items_error)



@adminRouter.callback_query(StateFilter(adminStates.AdminProductsManage.enter_data_items), F.data == "stop_upload_items")
async def stop_upload_items(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await call.message.edit_text(BotTexts.ADMIN_TEXTS.stop_upload_items_text.format(count=(await state.get_data())['count_add_items']))
    await state.clear()


@adminRouter.callback_query(F.data == "add_items")
async def add_items(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    categories = await DB.get_all_categories()
    if categories:
        await call.message.edit_text(BotTexts.ADMIN_TEXTS.select_category,
                                 reply_markup=BotButtons.ADMIN_INLINE.category_select_menu(BotTexts, categories).as_markup())
        await state.set_state(adminStates.AdminProductsManage.select_category_for_add_items)
    else:
        await call.answer(BotTexts.ADMIN_TEXTS.no_categories_available)


@adminRouter.callback_query(F.data.startswith("select_category:"), StateFilter(adminStates.AdminProductsManage.select_category_for_add_items))
async def select_category_for_add_items(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    positions = await DB.get_positions(cat_id=int(call.data.split(":")[1]), sub_cat_id=None)
    sub_categories = await DB.get_subcategories(cat_id=int(call.data.split(":")[1]))
    if sub_categories:
        await call.message.edit_text(
            BotTexts.ADMIN_TEXTS.select_subcategory,
            reply_markup=BotButtons.ADMIN_INLINE.subcategory_select_menu(BotTexts, subcategories=sub_categories, 
                                                                         positions=positions, is_for_edit_position=True).as_markup()
        )
        await state.set_state(adminStates.AdminProductsManage.select_subcategory_for_add_items)
    else:
        if positions:
            await call.message.edit_text(
                BotTexts.ADMIN_TEXTS.select_position,
                reply_markup=BotButtons.ADMIN_INLINE.position_select_menu(BotTexts, positions).as_markup(),
            )
            await state.set_state(adminStates.AdminProductsManage.select_position_for_add_items)
        else:
            await call.answer(BotTexts.ADMIN_TEXTS.no_positions_available_in_this_category)


@adminRouter.callback_query(F.data.startswith("select_subcategory:"), StateFilter(adminStates.AdminProductsManage.select_subcategory_for_add_items))
async def select_subcategory_for_add_items(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    positions = await DB.get_positions(sub_cat_id=int(call.data.split(":")[1]))
    if positions:
        await call.message.edit_text(
            BotTexts.ADMIN_TEXTS.select_position,
            reply_markup=BotButtons.ADMIN_INLINE.position_select_menu(BotTexts, positions).as_markup(),
        )
        await state.set_state(adminStates.AdminProductsManage.select_position_for_add_items)
    else:
        await call.answer(BotTexts.ADMIN_TEXTS.no_positions_available_in_this_subcategory)


@adminRouter.callback_query(F.data.startswith("select_position:"), StateFilter(adminStates.AdminProductsManage.select_position_for_add_items, 
                                                                               adminStates.AdminProductsManage.select_subcategory_for_add_items))
async def select_position_for_add_items(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    position = await DB.get_position(pos_id=int(call.data.split(":")[1]))
    await call.message.edit_text(BotTexts.ADMIN_TEXTS.enter_data_items["text_infinity" if position.item_type == "text" and position.is_infinity else position.item_type],
                                     reply_markup=BotButtons.ADMIN_INLINE.custom_button(BotTexts, "products_manage").as_markup())
    await state.set_state(adminStates.AdminProductsManage.enter_data_items)
    await state.update_data(position=position, count_add_items=0)


@adminRouter.callback_query(F.data == "del_item")
async def del_item(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    await call.message.edit_text(BotTexts.ADMIN_TEXTS.enter_item_id_for_delete,
                                 reply_markup=BotButtons.ADMIN_INLINE.custom_button(BotTexts, "products_manage").as_markup())
    await state.set_state(adminStates.AdminProductsManage.enter_item_id_for_delete)


@adminRouter.message(StateFilter(adminStates.AdminProductsManage.enter_item_id_for_delete))
async def enter_item_id_for_delete(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    if msg.text.isdigit():
        await state.clear()
        await DB.delete_item(int(msg.text))
        await msg.reply(BotTexts.ADMIN_TEXTS.success)
        await msg.answer(BotTexts.ADMIN_TEXTS.products_manage_text, 
                                 reply_markup=BotButtons.ADMIN_INLINE.products_manage(BotTexts).as_markup())
    else:
        await msg.reply(BotTexts.ADMIN_TEXTS.value_is_no_number,
                        reply_markup=BotButtons.ADMIN_INLINE.custom_button(BotTexts, "products_manage").as_markup())
        

@adminRouter.callback_query(F.data == "del_all_items")
async def del_all_items(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    await call.message.edit_text(BotTexts.ADMIN_TEXTS.del_all_items_text,
                                 reply_markup=BotButtons.ADMIN_INLINE.confirm(
                                     f"delete_all_items", "products_manage"
                                 ).as_markup())
    

@adminRouter.callback_query(F.data == "delete_all_items")
async def delete_all_items(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    await call.message.delete()
    await DB.delete_all_items()
    await utils.send_admins("all_items_are_deleted_alert",
            username=call.from_user.mention_html(),
        )
    await call.message.answer(BotTexts.ADMIN_TEXTS.products_manage_text, 
                     reply_markup=BotButtons.ADMIN_INLINE.products_manage(BotTexts).as_markup())