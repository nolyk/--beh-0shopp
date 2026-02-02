from aiogram import F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.data.loader import bot, userRouter, adminRouter, dp
from tgbot.data.config import BotButtons, BotConfig, BotImages, DB
from tgbot.data.config import BotTexts as BTs
from tgbot.utils import utils, models

import asyncio
import os


@dp.callback_query(F.data == "NONE")
async def none_callback(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer()


@userRouter.callback_query(F.data == "back_to_user_menu")
async def back_to_user_menu(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    await call.message.delete()
    if BotImages.START_PHOTO:
        await call.message.answer_photo(BotImages.START_PHOTO,
                            caption=BotTexts.TEXTS.main_menu.format(username=call.from_user.mention_html()),
                            reply_markup=await BotButtons.USERS_REPLY.main_menu(BotTexts, call.from_user.id, BotConfig.ADMINS))
    else:
        await call.message.answer(BotTexts.TEXTS.main_menu.format(username=call.from_user.mention_html()), 
                         reply_markup=await BotButtons.USERS_REPLY.main_menu(BotTexts, call.from_user.id, BotConfig.ADMINS))


@userRouter.message(Command("start"))
async def command_start(msg: Message, command: CommandObject, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    user = await DB.get_user(user_id=msg.from_user.id)
    kb = await BotButtons.USERS_REPLY.main_menu(BotTexts, msg.from_user.id, BotConfig.ADMINS)
    message_text = BotTexts.TEXTS.main_menu.format(username=msg.from_user.mention_html())
    settings = await DB.get_settings()
    if not command.args:
        if BotImages.START_PHOTO:
            await msg.answer_photo(BotImages.START_PHOTO,
                                caption=message_text,
                                reply_markup=kb)
        else:
            await msg.answer(message_text, reply_markup=kb)
    else:
        reffer_user_id = int(command.args)
        reffer = await DB.get_user(user_id=reffer_user_id)
        if reffer is None:
            if BotImages.START_PHOTO:
                await msg.answer_photo(BotImages.START_PHOTO,
                                       caption=message_text,
                                       reply_markup=kb)
            else:
                await msg.answer(message_text, reply_markup=kb)
        else:
            if user.ref_id is not None:
                await msg.answer(BotTexts.TEXTS.yes_reffer)
            else:
                if reffer.user_id == msg.from_user.id:
                    await msg.answer(BotTexts.TEXTS.invite_yourself)
                else:
                    await DB.update_user(user_id=msg.from_user.id, ref_id=reffer.user_id, ref_user_name=reffer.user_name, ref_full_name=reffer.full_name)
                    await DB.update_user(user_id=reffer.user_id, ref_count=reffer.ref_count + 1)

                    await bot.send_message(chat_id=reffer.user_id, text=BotTexts.TEXTS.new_refferal.format(user_name=user.user_name,
                                                       user_ref_count=reffer.ref_count + 1,
                                                       convert_ref=utils.numeral_noun_declension(reffer.ref_count + 1, BotTexts.TEXTS.ref_s)))

                    if BotImages.START_PHOTO:
                        await msg.answer_photo(BotImages.START_PHOTO,
                                            caption=message_text,
                                            reply_markup=kb)
                    else:
                        await msg.answer(message_text, reply_markup=kb)


@userRouter.message(F.text == BTs.Ru.BUTTONS.support)
async def open_support(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    settings = await DB.get_settings()
    if settings.support and settings.support != "-":
        text = BotTexts.TEXTS.support_text
        kb = (await BotButtons.USERS_INLINE.support(BotTexts)).as_markup()
    else:
        text = BotTexts.TEXTS.support_is_not_provided
        kb = BotButtons.USERS_INLINE.custom_button(BotTexts, "back_to_user_menu").as_markup()

    if BotImages.SUPPORT_PHOTO:
        await msg.answer_photo(BotImages.SUPPORT_PHOTO,
                               caption=text, reply_markup=kb)
    else:
        await msg.answer(text, reply_markup=kb)
        

@userRouter.callback_query(F.data == "support")
async def open_support_callback(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    settings = await DB.get_settings()
    if settings.support and settings.support != "-":
        text = BotTexts.TEXTS.support_text
        kb = (await BotButtons.USERS_INLINE.support(BotTexts)).as_markup()
    else:
        text = BotTexts.TEXTS.support_is_not_provided
        kb = BotButtons.USERS_INLINE.custom_button(BotTexts, "back_to_user_menu").as_markup()

    await call.message.delete()
    if BotImages.SUPPORT_PHOTO:
        await call.message.answer_photo(BotImages.SUPPORT_PHOTO,
                               caption=text, reply_markup=kb)
    else:
        await call.message.answer(text, reply_markup=kb)


@userRouter.message(F.text == BTs.Ru.BUTTONS.faq)
async def open_faq(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    settings = await DB.get_settings()
    if settings.faq_on and settings.faq and settings.faq != "-":
        text = settings.faq
        kb = BotButtons.USERS_INLINE.custom_button(BotTexts, "back_to_user_menu").as_markup()
    else:
        text = "❌ FAQ недоступна"
        kb = BotButtons.USERS_INLINE.custom_button(BotTexts, "back_to_user_menu").as_markup()

    if BotImages.SUPPORT_PHOTO:
        await msg.answer_photo(BotImages.SUPPORT_PHOTO,
                               caption=text, reply_markup=kb, parse_mode="HTML")
    else:
        await msg.answer(text, reply_markup=kb, parse_mode="HTML")


@userRouter.callback_query(F.data == "faq_view")
async def open_faq_callback(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    settings = await DB.get_settings()
    if settings.faq_on and settings.faq and settings.faq != "-":
        text = settings.faq
        kb = BotButtons.USERS_INLINE.close(BotTexts).as_markup()
    else:
        text = "❌ FAQ недоступна"
        kb = BotButtons.USERS_INLINE.custom_button(BotTexts, "back_to_user_menu").as_markup()

    await call.message.delete()
    if BotImages.SUPPORT_PHOTO:
        await call.message.answer_photo(BotImages.SUPPORT_PHOTO,
                               caption=text, reply_markup=kb, parse_mode="HTML")
    else:
        await call.message.answer(text, reply_markup=kb, parse_mode="HTML")


@userRouter.message(F.text == BTs.Ru.BUTTONS.buy)
async def buy(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    categories = await DB.get_all_categories()
    if categories:
        if BotImages.BUY_PHOTO:
            await msg.answer_photo(photo=BotImages.BUY_PHOTO, caption=BotTexts.TEXTS.available_cats,
                                   reply_markup=BotButtons.USERS_INLINE.select_category(BotTexts, categories).as_markup())
        else:
            await msg.answer(BotTexts.TEXTS.available_cats, 
                             reply_markup=BotButtons.USERS_INLINE.select_category(BotTexts, categories).as_markup())
    else:
        await msg.answer(BotTexts.TEXTS.no_cats,
                         reply_markup=BotButtons.USERS_INLINE.custom_button(BotTexts, "back_to_user_menu").as_markup())
        
        
@userRouter.callback_query(F.data == "buy")
async def buy_callback(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    categories = await DB.get_all_categories()
    await call.message.delete()
    if categories:
        if BotImages.BUY_PHOTO:
            await call.message.answer_photo(photo=BotImages.BUY_PHOTO, caption=BotTexts.TEXTS.available_cats,
                                   reply_markup=BotButtons.USERS_INLINE.select_category(BotTexts, categories).as_markup())
        else:
            await call.message.answer(BotTexts.TEXTS.available_cats, 
                             reply_markup=BotButtons.USERS_INLINE.select_category(BotTexts, categories).as_markup())
    else:
        await call.message.answer(BotTexts.TEXTS.no_cats,
                         reply_markup=BotButtons.USERS_INLINE.custom_button(BotTexts, "back_to_user_menu").as_markup())


@userRouter.callback_query(F.data.startswith("open_category:"))
async def open_category_callback(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    cat_id = int(call.data.split(":")[1])
    subcategories = await DB.get_subcategories(cat_id=cat_id)
    # Get positions that don't have subcategory (top-level positions)
    all_positions = await DB.get_positions(cat_id=cat_id)
    positions = [p for p in all_positions if p.sub_cat_id is None]
    
    await call.message.delete()
    if subcategories or positions:
        await call.message.answer(
            BotTexts.TEXTS.select_product,
            reply_markup=(await BotButtons.USERS_INLINE.select_subcategories_and_positions(BotTexts, subcategories, positions)).as_markup()
        )
    else:
        categories = await DB.get_all_categories()
        await call.message.answer(
            BotTexts.TEXTS.no_products,
            reply_markup=BotButtons.USERS_INLINE.select_category(BotTexts, categories).as_markup()
        )


@userRouter.callback_query(F.data.startswith("open_subcategory:"))
async def open_subcategory_callback(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    sub_cat_id = int(call.data.split(":")[1])
    
    # Get subcategory to find cat_id
    sub_cat = await DB.get_subcategory(sub_cat_id=sub_cat_id)
    if not sub_cat:
        await call.answer("Подкатегория не найдена")
        return
    
    positions = await DB.get_positions(cat_id=sub_cat.cat_id, sub_cat_id=sub_cat_id)
    
    await call.message.delete()
    if positions:
        await call.message.answer(
            BotTexts.TEXTS.select_product,
            reply_markup=(await BotButtons.USERS_INLINE.select_positions(BotTexts, positions)).as_markup()
        )
    else:
        await call.message.answer(
            BotTexts.TEXTS.no_products,
            reply_markup=BotButtons.USERS_INLINE.select_category(BotTexts, await DB.get_all_categories()).as_markup()
        )


@userRouter.callback_query(F.data.startswith("open_position:"))
async def open_position_callback(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    pos_id = int(call.data.split(":")[1])
    position = await DB.get_position(pos_id=pos_id)
    
    if not position:
        await call.answer("Позиция не найдена")
        return
    
    settings = await DB.get_settings()
    
    # Get price based on currency
    match settings.currency.value:
        case "usd":
            price = position.price_usd
        case "eur":
            price = position.price_eur
        case _:
            price = position.price_uzs
    
    text = BotTexts.TEXTS.position_info.format(
        name=position.name,
        description=position.description if position.description else "Нет описания",
        price=price,
        curr=BotConfig.CURRENCIES[settings.currency.value]['sign']
    )
    
    await call.message.delete()
    
    # Send with photo if available, otherwise send text only
    if position.photo:
        await call.message.answer_photo(
            photo=position.photo,
            caption=text,
            reply_markup=BotButtons.USERS_INLINE.position_buy(BotTexts, position).as_markup()
        )
    else:
        await call.message.answer(
            text,
            reply_markup=BotButtons.USERS_INLINE.position_buy(BotTexts, position).as_markup()
        )


@userRouter.callback_query(F.data == "close")
async def close_callback(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    await call.message.delete()
    if BotImages.START_PHOTO:
        await call.message.answer_photo(BotImages.START_PHOTO,
                            caption=BotTexts.TEXTS.main_menu.format(username=call.from_user.mention_html()),
                            reply_markup=await BotButtons.USERS_REPLY.main_menu(BotTexts, call.from_user.id, BotConfig.ADMINS))
    else:
        await call.message.answer(BotTexts.TEXTS.main_menu.format(username=call.from_user.mention_html()), 
                         reply_markup=await BotButtons.USERS_REPLY.main_menu(BotTexts, call.from_user.id, BotConfig.ADMINS))


@adminRouter.message(Command(commands=['getFileId']))
async def getFileIdCommand(msg: Message, state: FSMContext, BotTexts):
    await state.clear()
    message = msg.reply_to_message
    media_type = ""
    
    if message.photo:
        media_type = "Фото"
        file_id = message.photo[-1].file_id
    elif message.animation:
        media_type = "Гиф"
        file_id = message.animation.file_id
    elif message.video:
        media_type = "Видео"
        file_id = message.video.file_id
    else:
        media_type = "Файл"
        # document
        file_id = message.document.file_id
    
    await msg.reply(f"<b>Тип медиа: <code>{media_type}</code>\nFILE_ID: <code>{file_id}</code></b>")

@adminRouter.message(Command(commands=['admin', 'adm', 'a']))
@adminRouter.message(F.text == BTs.Ru.BUTTONS.admin_panel)
async def admin_panel(msg: Message, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    await msg.answer(BotTexts.ADMIN_TEXTS.welcome_to_the_admin_panel,
                     reply_markup=BotButtons.ADMIN_INLINE.admin_panel(BotTexts).as_markup())
    
    
@adminRouter.callback_query(F.data == "admin_panel")
async def admin_panel_callback(call: CallbackQuery, state: FSMContext, BotTexts: BTs.Ru):
    await state.clear()
    await call.message.delete()
    await call.message.answer(BotTexts.ADMIN_TEXTS.welcome_to_the_admin_panel,
                     reply_markup=BotButtons.ADMIN_INLINE.admin_panel(BotTexts).as_markup())
