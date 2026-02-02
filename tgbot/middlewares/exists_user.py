from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from tgbot.data.config import DB, BotButtons
from tgbot.utils.utils import send_admins, get_language

from traceback import print_exc
from loguru import logger
from typing import Any, Callable, Dict, Awaitable


class ExistsUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        update: Update = data['event_update']
        user = data["event_from_user"]
        if update.message:
            logger.info(f"{user.full_name} - {update.message.text}")
        else:
            logger.info(f"{user.full_name} - {update.callback_query.data} (Callback)")
        try:
            if user is not None and not user.is_bot:
                settings = await DB.get_settings()

                db_user = await DB.get_user(user_id=user.id)

                # Если пользователя нет — регистрируем, отправляем алерты/выбор языка
                if db_user is None:
                    await DB.register_user(user.id, user.username, user.full_name)
                    BotTexts = await get_language(user.id)
                    if not settings.is_work:
                        await update.message.answer(
                            BotTexts.TEXTS.choose_language,
                            reply_markup=BotButtons.USERS_INLINE.choose_language(BotTexts).as_markup()
                        )
                else:
                    # Кешируем объект user
                    self.user = db_user
                    BotTexts = await get_language(user.id)
                    # Проверяем бан
                    if self.user.is_ban:
                        return await event.answer(BotTexts.TEXTS.is_ban_text)

                    # Обновляем только если что-то поменялось
                    updates = {}
                    if self.user.user_name != user.full_name:
                        updates['full_name'] = user.full_name
                    # Проверяем username отдельно
                    new_username = user.username or ""
                    if new_username != self.user.user_name:
                        updates['user_name'] = new_username

                    # Если что-то поменялось — делаем update
                    if updates:
                        await DB.update_user(user.id, **updates)

        except Exception:
            print_exc()
        
        return await handler(event, data)