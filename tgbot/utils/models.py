from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import BigInteger, String, Boolean, Integer, Enum, Float, Column
from sqlalchemy import select, insert, text

from tgbot.data.config import BotConfig

import enum
import time
import os
import logging

logger = logging.getLogger(__name__)

# Инициализация асинхронного движка для SQLite
db_path = os.path.join(os.path.dirname(__file__), '../../database.db')
engine = create_async_engine(f'sqlite+aiosqlite:///{db_path}')

# Создаем асинхронный фабричный метод для сессий
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Currencies(enum.Enum):
    uzs = "uzs"
    usd = "usd"
    eur = "eur"
    

class Languages(enum.Enum):
    ru = "ru"
    en = "en"
    ua = "ua"


class Keyboards(enum.Enum):
    Reply = "Reply"
    Inline = "Inline"


class User(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True)
    is_ban = Column(Boolean, default=False)
    user_name = Column(String)
    full_name = Column(String)
    balance_uzs = Column(Float, default=0)
    balance_usd = Column(Float, default=0)
    balance_eur = Column(Float, default=0)
    language: Mapped[Languages] = Column(Enum(Languages), default=Languages.ru)
    total_refill = Column(Float, default=0)
    count_refills = Column(Integer, default=0)
    reg_date = Column(String)
    reg_date_unix = Column(BigInteger)
    ref_lvl = Column(Integer, default=1)
    ref_id = Column(BigInteger)
    ref_user_name = Column(String)
    ref_full_name = Column(String)
    ref_count = Column(Integer, default=0)
    ref_earn_uzs = Column(Float, default=0)
    ref_earn_usd = Column(Float, default=0)
    ref_earn_eur = Column(Float, default=0)


class Settings(Base):
    __tablename__ = "settings"

    settings = Column(String, default="main", primary_key=True)
    is_work = Column(Boolean, default=True)
    faq = Column(String, default="❓ FAQ не установлена")
    faq_on = Column(Boolean, default=False)
    chat = Column(String)
    news = Column(String)
    support = Column(String)
    support_ls = Column(String, default="-")
    profit_day = Column(Integer, default=0)
    profit_week = Column(Integer, default=0)
    currency: Mapped[Currencies] = Column(Enum(Currencies), default=Currencies.uzs)
    keyboard: Mapped[Keyboards] = Column(Enum(Keyboards), default=Keyboards.Reply)
    default_lang: Mapped[Languages] = Column(Enum(Languages), default=Languages.ru)
    custom_pay_method = Column(String, default="Custom Pay Method")
    custom_pay_method_text = Column(String, default="Transfer to card <code>123456789</code> to top up your balance.")
    custom_pay_method_min_amount = Column(Float, default=0.0)
    is_custom_pay_method_receipt_on = Column(Boolean, default=False)
    is_custom_pay_method_on = Column(Boolean, default=False)
    photo_main_menu = Column(String, default=None)
    photo_support = Column(String, default=None)
    photo_buy = Column(String, default=None)


class Refill(Base):
    __tablename__ = "refills"

    user_id = Column(BigInteger)
    amount = Column(Float)
    receipt = Column(String, primary_key=True)
    way = Column(String)
    date = Column(String)
    date_unix = Column(BigInteger)
    pay_url = Column(String)
    second_amount = Column(Float)
    currency = Column(Enum(Currencies))
    is_finish = Column(Boolean, default=False)
    under_date = Column(BigInteger)


class Rates(Base):
    __tablename__ = "rates"
    
    settings = Column(String, default="rates", primary_key=True)
    usd_uzs = Column(Float, default=0.0)
    usd_eur = Column(Float, default=0.0)
    eur_uzs = Column(Float, default=0.0)
    eur_usd = Column(Float, default=0.0)
    uzs_usd = Column(Float, default=0.0)
    uzs_eur = Column(Float, default=0.0)


class Purchase(Base):
    __tablename__ = "purchases"

    user_id = Column(BigInteger)
    receipt = Column(String, primary_key=True)
    count = Column(Integer)
    price_uzs = Column(Float)
    price_usd = Column(Float)
    price_eur = Column(Float)
    pos_id = Column(BigInteger)
    item = Column(String)
    date = Column(String)
    unix = Column(BigInteger)


class AdButton(Base):
    __tablename__ = "ad_buttons"

    button_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    text = Column(String)
    photo = Column(String)
    links = Column(String, default=None)


class Position(Base):
    __tablename__ = "positions"

    pos_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    price_uzs  = Column(Float)
    price_usd  = Column(Float)
    price_eur  = Column(Float)
    description = Column(String)
    photo = Column(String)
    cat_id = Column(Integer)
    sub_cat_id = Column(Integer)
    is_infinity = Column(Boolean)
    item_type = Column(String, default="text")


class SubCategory(Base):
    __tablename__ = "sub_categories"

    sub_cat_id = Column(Integer, primary_key=True, autoincrement=True)
    cat_id = Column(Integer)
    name = Column(String)


class Promocode(Base):
    __tablename__ = "promocodes"

    name = Column(String, primary_key=True)
    uses = Column(Integer)
    discount_uzs = Column(Float)
    discount_usd = Column(Float)
    discount_eur = Column(Float)


class MailButton(Base):
    __tablename__ = "mail_buttons"

    button_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    button_type = Column(String)
    

class Item(Base):
    __tablename__ = "items"

    item_id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(String)
    pos_id = Column(Integer)
    cat_id = Column(Integer)
    date = Column(String)
    file_id = Column(String)


class ContestsSettings(Base):
    __tablename__ = "contests_settings"

    settings = Column(String, default="main", primary_key=True)
    winners_num = Column(Integer, default=1)
    prize = Column(Float, default=100)
    purchases_num = Column(Integer, default=0)
    refills_num = Column(Integer, default=0)
    channels_ids = Column(String)
    members_num = Column(Integer, default=10)
    end_time = Column(BigInteger)


class ContestMember(Base):
    __tablename__ = "contests_members"

    member_id = Column(Integer, primary_key=True, autoincrement=True)
    contest_id = Column(Integer)
    user_id = Column(BigInteger)


class Contest(Base):
    __tablename__ = "contests"

    contest_id = Column(Integer, autoincrement=True, primary_key=True)
    prize = Column(Float)
    currency: Mapped[Currencies] = Column(Enum(Currencies), default=Currencies.uzs)
    members_num = Column(Integer)
    end_time = Column(BigInteger)
    winners_num = Column(Integer)
    channels_ids = Column(String)
    refills_num = Column(Integer, default=0)
    purchases_num = Column(Integer, default=0)


class Category(Base):
    __tablename__ = "categories"

    cat_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class ActivePromocode(Base):
    __tablename__ = "active_promocodes"

    use_id = Column(Integer, primary_key=True, autoincrement=True)
    promocode_name = Column(String)
    user_id = Column(BigInteger)


async def async_main() -> None:
    async with engine.begin() as conn:
        logger.info("Initializing database...")
        # Create tables if they don't exist (no drop, preserve existing data)
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created/verified")

        if len((await conn.execute(select(Rates))).scalars().all()) == 0:
            logger.info("Creating default Rates entry")
            await conn.execute(insert(Rates))
        if len((await conn.execute(select(Settings))).scalars().all()) == 0:
            logger.info("Creating default Settings entry")
            await conn.execute(insert(Settings).values(
                profit_day=int(time.time()),
                profit_week=int(time.time()),
                support_ls="-"
            ))
        if len((await conn.execute(select(ContestsSettings))).scalars().all()) == 0:
            logger.info("Creating default ContestsSettings entry")
            await conn.execute(insert(ContestsSettings).values(
                channels_ids="-",
                end_time=0,
            ))
                
        await conn.commit()
        logger.info("Database initialization complete")