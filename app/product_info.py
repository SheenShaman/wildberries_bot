import requests


def get_product_info(article):
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}"
    response = requests.get(url)
    product_info = response.json()
    try:
        product_data = {
            "Название": product_info["data"]["products"][0]["name"],
            "Артикул": product_info["data"]["products"][0]["id"],
            "Цена": f'{product_info["data"]["products"][0]["salePriceU"] // 100} ₽',
            "Рейтинг товара": f'{product_info["data"]["products"][0]["reviewRating"]} / 5',
            "Количество товара": f'{product_info["data"]["products"][0]["sizes"][0]["stocks"][0]["qty"]} шт.'
        }
        return product_data
    except IndexError:
        return "Неверный артикул"
