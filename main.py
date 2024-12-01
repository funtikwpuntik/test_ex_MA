import json
import requests

headers = {
    'authorization': 'Basic NGxhcHltb2JpbGU6eEo5dzFRMyhy',
}
cookies = {
    'selected_city_code': '0000073738',
}
params = {
    'category_id': '3',
    'count': '10',
    'page': '1',
    'sort': 'popular',
    'sign': '5ac269b9f10031ac9ca757350c4624c8',
    'token': '9f5171c973cadf65e6e3418e5c6f10db',
}
signs_catalog = [
    '5ac269b9f10031ac9ca757350c4624c8',
    '358daabe7140932ed0c86a86abb8a89f',
    '4fda0235cfd5610fecf73cf201e8f2c7',
    '252808faa26becb8372711769a69190d',
    'bdcab6ccc1135db9249d8258cbf85f4a',
    '02720b4a9401e920c0b879a2efd58d4f',
    '60f4fcf5ed7d01cbc2d22137daea4470',
    'b459ac3cea55bee07761dc4caa15b2cc',
    'b0b05ba29fa4ab0c7d3cdb6454a0b5e2',
    '32cbacf58b176dc995701d97e8392f15',
]
signs_info=[
    'd4f5b31415538b71fca1cd063d1f7631',
    '5c62a3558322534af1e77a3a18bba931',
    'ec30b1c62b0eec2a12cfd437e6408632',
    '557677fc34120cff64786777bd4435ca',
    '234874a2ac65c8d803ba72642a5b2cc2',
    'be9f3e80d288e5e5ae74b533a04b14ba',
    '97d8103d898151d54bf9709a6335fda5',
    '599923e546d25345f8356dba30ec9d32',
    'd13c106eb72891097cfba0f73b3bc151',
    'be1f5c6b95e7a2bfa70fc64cd8b11cf6',
]

goods = {}
for page in range(1,11): # в запросе 10 товаров, поэтому кол-во запросов 10
    params['page'] = page
    params['sign'] = signs_catalog[page-1]
    goods_list = requests.get("https://4lapy.ru/api/v2/catalog/product/list/",
                             headers=headers, params=params, cookies=cookies).json()['data']['goods']
    count = 0
    data = {
        'sign': signs_info[page-1],
        'token': '9f5171c973cadf65e6e3418e5c6f10db',
    }

    for good in goods_list:

        # Записываем данные для запроса цен
        data[f'offers[{count}]'] = good['id']
        count += 1
        for variant in good['packingVariants']:
            # Записываем первичные данные
            if variant['isAvailable']:
                if not goods.get(good['id']):
                    goods[good['id']] = {
                        'id': variant['id'],
                        'title': variant['title'],
                        'webpage': variant['webpage'].replace('https://old.', 'https://'),
                        'brand': variant['brand_name'],
                        'pack': variant['in_pack'],
                    }
            data[f'offers[{count}]'] = variant['id']
            count += 1

    res = requests.post(
        'https://4lapy.ru/api/v2/catalog/product/info-list/',
        headers=headers,
        data=data,
    ).json()
    # Запрос для цен
    goods_info = res['data']['products']

    # Записываем цены
    for good in goods:
        for good_info in goods_info:
            for variant in good_info['variants']:
                if variant['id'] == goods[good]['id']:
                    goods[good]['discount_price'] = variant['price']['actual'] if variant['price']['old'] else 0
                    goods[good]['price'] = variant['price']['old'] if variant['price']['old'] else variant['price']['actual']
                    goods[good]['singleItemPackDiscountPrice'] = variant['price']['singleItemPackDiscountPrice']
                    continue

with open('data.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(goods, indent=4, ensure_ascii=False))