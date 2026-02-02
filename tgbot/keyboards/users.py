from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot import utils
from tgbot.data import config as config_file
from tgbot.data import loader

class InlineButtons:
    async def profile_menu(self, texts):
        builder = InlineKeyboardBuilder()
        settings = await config_file.DB.get_settings()
            
        builder.row(
            InlineKeyboardButton(
                text=texts.BUTTONS.activate_promo,
                callback_data="activate_promo"),
            InlineKeyboardButton(
                text=texts.BUTTONS.purchases_history,
                callback_data="purchases_history",
            )
        )
        builder.row(InlineKeyboardButton(
            text=texts.BUTTONS.back,
            callback_data="back_to_user_menu"
        ))
        return builder

    async def support(self, texts):
        builder = InlineKeyboardBuilder()
        settings = await config_file.DB.get_settings()
        
        # Add support and FAQ buttons in one row
        kb = []
        if settings.support and settings.support != "-":
            kb.append(
                InlineKeyboardButton(
                    text=texts.BUTTONS.support_text,
                    url=settings.support
                )
            )
        
        if settings.faq_on and settings.faq and settings.faq != "-":
            kb.append(
                InlineKeyboardButton(
                    text=texts.BUTTONS.faq,
                    callback_data="faq_view"
                )
            )
        
        if kb:
            builder.row(*kb)
        
        builder.row(InlineKeyboardButton(
            text=texts.BUTTONS.back,
            callback_data="back_to_user_menu"
        ))
        return builder

    async def faq(self, texts):
        builder = InlineKeyboardBuilder()
        settings = await config_file.DB.get_settings()
        kb = []
        if settings.news and settings.news != "-":
            kb.append(
                InlineKeyboardButton(
                    text=texts.BUTTONS.faq_news_inl,
                    url=settings.news
                )
            )
        if settings.chat and settings.chat != "-":
            kb.append(
                InlineKeyboardButton(
                    text=texts.BUTTONS.faq_chat_inl,
                    url=settings.chat
                )
            )
        builder.add(*kb)
        builder.row(InlineKeyboardButton(
            text=texts.BUTTONS.back,
            callback_data="back_to_user_menu"
        ))
        return builder

    def close(self, texts):
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(
                text=texts.BUTTONS.close,
                callback_data="close",
            )
        )

        return builder

    async def get_refill_kb(self, texts, payments):
        builder = InlineKeyboardBuilder()
        for payment in payments:
            if payment == "custom_pay_method":
                settings = await config_file.DB.get_settings()
                builder.add(InlineKeyboardButton(
                    text=settings.custom_pay_method,
                    callback_data="refill:custom_pay_method",
                ))
            else:
                builder.add(
                    InlineKeyboardButton(
                        text=texts.TEXTS.payments_names[payment],
                        callback_data=f"refill:{payment}",
                    )
                )
        builder.adjust(2)
        builder.row(InlineKeyboardButton(
            text=texts.BUTTONS.back,
            callback_data="back_to_user_menu"
        ))
        return builder

    def custom_button(self, texts, callback_data, name=None):
        if not name:
            name = texts.BUTTONS.back
        return InlineKeyboardBuilder().button(text=name, callback_data=callback_data)

    def refill_inl(self, texts, way, amount, url, pay_id, second_amount):
        builder = InlineKeyboardBuilder()
        builder.button(text=texts.BUTTONS.refill_link_inl, url=url)
        builder.row(InlineKeyboardButton(text=texts.BUTTONS.refill_check_inl, callback_data=f"check_pay:{way}:{amount}:{pay_id}:{second_amount}"))
        builder.row(InlineKeyboardButton(text=texts.BUTTONS.cancel, callback_data=f"cancel_pay:{pay_id}"))
        return builder
    
    def custom_pay_method_check(self, texts, pay_id):
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(
            text=texts.BUTTONS.send_payment_to_check,
            callback_data=f"check_custom_pay_method:{pay_id}"
        ))
        builder.row(InlineKeyboardButton(
            text=texts.BUTTONS.cancel, 
            callback_data=f"cancel_pay:{pay_id}"
        ))
        return builder

    def ad_buttons_links_buttons(self, texts, links, is_back=False):
        try:
            builder = InlineKeyboardBuilder()
            if not links and is_back:
                builder.row(
                    InlineKeyboardButton(
                        text=texts.BUTTONS.back,
                        callback_data="back_to_user_menu",
                    )
                )
                return builder.as_markup()
            links = links.split("\n")
            if links:
                for link in links:
                    try:
                        name, url = link.split("|")
                        try:
                            builder.row(InlineKeyboardButton(text=name, url=url.strip()))
                        except:
                            continue
                    except ValueError:
                        continue
                if is_back:
                    builder.row(
                        InlineKeyboardButton(
                            text=texts.BUTTONS.back,
                            callback_data="back_to_user_menu",
                        )
                    )
                return builder.as_markup()
            else:
                name, url = links.split("|")
                if name and url:
                    try:
                        builder.row(InlineKeyboardButton(text=name, url=url.strip()))
                        if is_back:
                            builder.row(
                                InlineKeyboardButton(
                                    text=texts.BUTTONS.back,
                                    callback_data="back_to_user_menu",
                                )
                            )
                        return builder.as_markup()
                    except:
                        return None
                else:
                    return None
        except:
            return None
        
    def select_category(self, texts, categories):
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text=texts.BUTTONS.search_product, callback_data="search_product"))
        for category in categories:
            builder.add(InlineKeyboardButton(text=category.name, callback_data=f"open_category:{category.cat_id}"))
        builder.adjust(1)
        builder.row(InlineKeyboardButton(text=texts.BUTTONS.back, callback_data="back_to_user_menu"))
        return builder

    async def select_subcategories_and_positions(self, texts, subcategories, positions):
        builder = InlineKeyboardBuilder()
        settings = await config_file.DB.get_settings()

        for sub_category in subcategories:
            builder.add(InlineKeyboardButton(text=sub_category.name, callback_data=f"open_subcategory:{sub_category.sub_cat_id}"))
        for position in positions:
            if position.sub_cat_id is not None:
                continue
            match settings.currency.value:
                case "uzs":
                    price = position.price_uzs
                case "usd":
                    price = position.price_usd
                case "eur":
                    price = position.price_eur
            if position.is_infinity:
                items = texts.BUTTONS.nolimit
            else:
                items = f"{len(await config_file.DB.get_items(pos_id=position.pos_id))} {texts.BUTTONS.pcs}"
            builder.add(InlineKeyboardButton(text=texts.BUTTONS.position_button_name.format(
                name=position.name,
                price=price,
                curr=config_file.BotConfig.CURRENCIES[settings.currency.value]['sign'],
                items=items,
            ), callback_data=f"open_position:{position.pos_id}"))
        builder.adjust(1)
        builder.row(InlineKeyboardButton(text=texts.BUTTONS.back, callback_data=f"buy"))
        return builder

    async def select_positions(self, texts, positions, back_callback=None):
        builder = InlineKeyboardBuilder()
        settings = await config_file.DB.get_settings()
        for position in positions:
            match settings.currency.value:
                case "uzs":
                    price = position.price_uzs
                case "usd":
                    price = position.price_usd
                case "eur":
                    price = position.price_eur
            if position.is_infinity:
                items = texts.BUTTONS.nolimit
            else:
                items = f"{len(await config_file.DB.get_items(pos_id=position.pos_id))} {texts.BUTTONS.pcs}"
            builder.add(InlineKeyboardButton(text=texts.BUTTONS.position_button_name.format(
                name=position.name,
                price=price,
                curr=config_file.BotConfig.CURRENCIES[settings.currency.value]['sign'],
                items=items,
            ), callback_data=f"open_position:{position.pos_id}"))
        builder.adjust(1)
        # Если back_callback не указан, используем стандартное возвращение к категории
        if back_callback is None:
            builder.row(InlineKeyboardButton(text=texts.BUTTONS.back, callback_data=f"open_category:{positions[0].cat_id}"))
        else:
            builder.row(InlineKeyboardButton(text=texts.BUTTONS.back, callback_data=back_callback))
        return builder

    def position_buy(self, texts, position):
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text=texts.BUTTONS.back, callback_data=f"open_subcategory:{position.sub_cat_id}" if position.sub_cat_id else f"open_category:{position.cat_id}"))    
        return builder
    
    def confirm_buy_item(self, position_id, count):
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text="✅", callback_data=f"buy_item_confirm:{position_id}:{count}"),
                    InlineKeyboardButton(text="❌", callback_data=f"open_position:{position_id}"))
        return builder
    
    def choose_contest(self, texts, contests):
        builder = InlineKeyboardBuilder()
        for contest in contests:
            end_time = utils.utils.get_time_for_end_contest(contest, texts.TEXTS.day_s)
            builder.row(InlineKeyboardButton(
                text=f"#{contest.contest_id} 🎉 | {contest.prize}{config_file.BotConfig.CURRENCIES[contest.currency.value]['sign']} | {end_time}",
                callback_data=f"contest_view:{contest.contest_id}"
            ))
        builder.row(InlineKeyboardButton(
            text=texts.BUTTONS.back,
            callback_data="back_to_user_menu"
        ))
        return builder
    
    async def contest_inl(self, texts, contest, user):
        builder = InlineKeyboardBuilder()
        purchases = (await config_file.DB.get_purchases_stats_for_user(user.user_id))['count_purchases']
        count_success, count_conditions, channels_count = 0, 0, 0

        if contest.refills_num > 0:
            count_conditions += 1
            if user.count_refills >= contest.refills_num:
                count_success += 1
        if contest.purchases_num > 0:
            count_conditions += 1
            if purchases >= contest.purchases_num:
                count_success += 1
        if len(utils.utils.get_channels(contest.channels_ids)) > 0:
            count_conditions += 1
            channels_ids = utils.utils.get_channels(contest.channels_ids)
            for channel_id in channels_ids:
                user_status = await loader.bot.get_chat_member(chat_id=channel_id, user_id=user.user_id)
                if user_status.status != 'left':
                    channels_count += 1

            if channels_count == len(channels_ids):
                count_success += 1

        if count_success == count_conditions:
            builder.row(InlineKeyboardButton(text=texts.BUTTONS.contest_enter, 
                                             callback_data=f"contest_enter:{contest.contest_id}"))
        else:
            builder.row(InlineKeyboardButton(
                text=texts.BUTTONS.you_not_completed_all_conditions.format(
                    count=count_success,
                    count_conditions=count_conditions    
                ),
                callback_data="NONE"))
        builder.row(InlineKeyboardButton(
            text=texts.BUTTONS.back,
            callback_data="back_to_user_menu"
        ))
        return builder
    
    def choose_language(self, texts):
        builder = InlineKeyboardBuilder()
        for language in config_file.BotConfig.LANGUAGES:
            builder.row(
                InlineKeyboardButton(
                    text=language['name'],
                    callback_data=f"change_language:{language['language']}"
                )
            )
        builder.row(InlineKeyboardButton(
            text=texts.BUTTONS.back,
            callback_data="profile"
        ))
        return builder
    
    async def sub_kb(self, texts, bot, channels):
        builder = InlineKeyboardBuilder()
        for channel_id in channels:
            channel = await bot.get_chat(chat_id=channel_id)
            try:
                link = "https://t.me/" + channel.username
            except:
                try:
                    link = channel.invite_link
                except:
                    link = (await bot.create_chat_invite_link(chat_id=channel_id)).invite_link
            builder.row(InlineKeyboardButton(text=channel.title, url=link))
        builder.row(InlineKeyboardButton(text=texts.BUTTONS.check_sub, callback_data="check_sub"))
        return builder
    

class ReplyButtons:
    async def main_menu(self, texts, user_id, admins):
        settings = await config_file.DB.get_settings()
        ad_buttons = await config_file.DB.get_ad_buttons()
        if settings.keyboard.value == "Reply":
            kb = [
                [KeyboardButton(text=texts.BUTTONS.buy), KeyboardButton(text=texts.BUTTONS.support)],
            ]
            if settings.faq_on and settings.faq and settings.faq != "-":
                kb.append([KeyboardButton(text=texts.BUTTONS.faq)])
            if user_id in admins:
                kb.append([KeyboardButton(text=texts.BUTTONS.admin_panel),])
            
            for button in ad_buttons:
                kb.append([KeyboardButton(text=button.name)])

            keyboard = ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
                input_field_placeholder=texts.BUTTONS.choose_action
            )
        else:
            builder = InlineKeyboardBuilder()
            builder.row(
                InlineKeyboardButton(text=texts.BUTTONS.buy, callback_data="buy"),
                InlineKeyboardButton(text=texts.BUTTONS.support, callback_data="support")
            )
            if settings.faq_on and settings.faq and settings.faq != "-":
                builder.row(
                    InlineKeyboardButton(text=texts.BUTTONS.faq, callback_data="faq_view")
                )
            builder.row(
                InlineKeyboardButton(text="📍 Локация", url="https://maps.google.com/?q=69.230509,41.210518&z=16"),
                InlineKeyboardButton(text="💬 Отзывы", url="https://t.me/Veloremontsergeli")
            )
            if user_id in admins:
                builder.row(InlineKeyboardButton(text=texts.BUTTONS.admin_panel, callback_data="admin_panel"))

            for button in ad_buttons:
                builder.row(InlineKeyboardButton(text=button.name, callback_data=f"ad_button_open:{button.button_id}"))

            keyboard = builder.as_markup()

        return keyboard
    
    