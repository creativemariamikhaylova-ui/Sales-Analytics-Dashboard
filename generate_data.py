import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

os.makedirs('data', exist_ok=True)

print("Генерация данных...")

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
num_records = 10000

categories = ['Электроника', 'Одежда', 'Книги', 'Дом и сад', 'Спорт']
products = {
    'Электроника': ['Смартфон', 'Ноутбук', 'Планшет', 'Наушники', 'Умные часы'],
    'Одежда': ['Футболка', 'Джинсы', 'Куртка', 'Кроссовки', 'Платье'],
    'Книги': ['Роман', 'Учебник', 'Детектив', 'Фантастика', 'Биография'],
    'Дом и сад': ['Посуда', 'Инструменты', 'Декор', 'Текстиль', 'Мебель'],
    'Спорт': ['Гантели', 'Коврик', 'Мяч', 'Велосипед', 'Форма']
}

regions = ['Москва', 'СПб', 'Новосибирск', 'Екатеринбург', 'Казань']

data = []
for _ in range(num_records):
    category = random.choice(categories)
    product = random.choice(products[category])
    date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    price = random.randint(500, 100000)
    quantity = random.randint(1, 10)
    region = random.choice(regions)
    customer_type = random.choice(['Новый', 'Постоянный'])

    data.append([
        date.strftime('%Y-%m-%d'),
        category,
        product,
        price,
        quantity,
        price * quantity,
        region,
        customer_type
    ])

df = pd.DataFrame(data, columns=[
    'Дата', 'Категория', 'Продукт', 'Цена', 'Количество',
    'Выручка', 'Регион', 'Тип клиента'
])

df.to_csv('data/sales_data.csv', index=False, encoding='utf-8-sig')
print(f"Сгенерировано {num_records} записей")
print(f"Файл сохранен: {os.path.abspath('data/sales_data.csv')}")

print("\n Первые 5 записей:")
print(df.head())