import aiohttp

async def get_exchanges(amount: float, cur1: str, cur2: str):
    if float(amount) == 0.0:
        return 0.0

    async with aiohttp.ClientSession() as session:
        ress = await session.get(f'https://api.exchangerate-api.com/v4/latest/{cur1}')
        res = await ress.json()
        await session.close()

        rate = res['rates'][cur2]

    return float(rate)

async def get_def_exchanges():
    rate_usd_to_uzs = float(await get_exchanges(1, 'USD', 'UZS'))
    rate_usd_to_eur = float(await get_exchanges(1, 'USD', 'EUR'))
    rate_eur_to_uzs = float(await get_exchanges(1, 'EUR', 'UZS'))
    rate_eur_to_usd = float(await get_exchanges(1, 'EUR', 'USD'))
    rate_uzs_to_usd = float(await get_exchanges(1, 'UZS', 'USD'))
    rate_uzs_to_eur = float(await get_exchanges(1, 'UZS', 'EUR'))

    return rate_usd_to_uzs, rate_usd_to_eur, rate_eur_to_uzs, rate_eur_to_usd, rate_uzs_to_usd, rate_uzs_to_eur
