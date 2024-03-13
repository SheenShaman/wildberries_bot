import requests


def get_product_info(article):
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}"
    # url = "https://card.wb.ru/cards/v1/detail"
    # params = {
    #     "appType": 1,
    #     "curr": "rub",
    #     "dest": -1257786,
    #     "spp": 30,
    #     "nm": article
    # }
    response = requests.get(url)
    product_info = response.json()
    try:
        product_data = {
            "название": product_info["data"]["products"][0]["name"],
            "артикул": product_info["data"]["products"][0]["id"],
            "цена": f'{product_info["data"]["products"][0]["salePriceU"] // 100} ₽',
            "рейтинг товара": f'{product_info["data"]["products"][0]["reviewRating"]} / 5',
            "количество товара": f'{product_info["data"]["products"][0]["sizes"][0]["stocks"][0]["qty"]} шт.'
        }
        return product_data
    except IndexError:
        return "Неверный артикул"


print(get_product_info(211695539))
