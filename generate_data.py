import pandas as pd
import random
from faker import Faker

fake = Faker("uk_UA")

# --- Імена ---
male_first_names = ["Олександр", "Андрій", "Сергій", "Іван", "Михайло", "Василь", "Володимир", "Роман", "Богдан", "Тарас"]
female_first_names = ["Олена", "Ірина", "Наталія", "Марина", "Тетяна", "Ольга", "Анна", "Юлія", "Катерина", "Світлана"]
male_last_names = ["Шевченко", "Коваль", "Бондаренко", "Кравчук", "Мельник", "Петренко", "Савченко", "Захарченко", "Гриценко", "Романюк"]
female_last_names = [ln + "а" if not ln.endswith("ко") else ln for ln in male_last_names]

# --- Категорії та продукти ---
categories = {
    "Ноутбуки": ["Lenovo IdeaPad 3", "HP Pavilion 15", "Dell Inspiron 14", "ASUS VivoBook 17", "Acer Aspire 7", "Apple MacBook Air"],
    "Монітори": ["Samsung Curved 27\"", "LG UltraGear 24\"", "Acer Nitro VG240Y", "Dell P2419H", "Philips 243V7Q"],
    "Периферія": ["Logitech K380", "Razer DeathAdder", "HyperX Cloud Stinger", "Genius SlimStar", "SteelSeries Apex 3"],
    "Офісна техніка": ["HP LaserJet Pro M15w", "Canon Pixma MG3650", "Brother DCP-L2532DW", "Epson EcoTank L3250"],
    "Смартфони": ["iPhone 13", "Samsung Galaxy A54", "Xiaomi Redmi Note 12", "OnePlus Nord CE", "Realme 11 Pro"],
    "Планшети": ["Apple iPad 10.2", "Samsung Galaxy Tab S6", "Lenovo Tab M10", "Xiaomi Pad 6"],
    "Аудіо": ["JBL Flip 6", "Sony WH-1000XM4", "Beats Studio Buds", "Marshall Emberton", "Xiaomi Mi Portable Speaker"],
    "Телевізори": ["Samsung QLED 55\"", "LG OLED C1 48\"", "Sony Bravia X80J", "Philips 58PUS8507", "Xiaomi Mi TV P1 50\""],
    "Побутова техніка": ["LG GA-B509", "Samsung WW80T", "Bosch Serie 4", "Tefal Express Steam", "Philips Daily Collection"]
}

product_list = []
product_prices = {}
for category, items in categories.items():
    for item in items:
        product_list.append({"назва": item, "категорія": category})
        product_prices[item] = random.randint(1000, 30000)

# --- Розподіл міст за населенням (ваги) ---
city_population_share = {
    "Київ": 15,
    "Харків": 10,
    "Одеса": 8,
    "Дніпро": 8,
    "Львів": 7,
    "Запоріжжя": 5,
    "Кривий Ріг": 4,
    "Миколаїв": 3,
    "Маріуполь": 3,
    "Вінниця": 3,
    "Херсон": 2,
    "Чернігів": 2,
    "Полтава": 2,
    "Черкаси": 2,
    "Житомир": 2,
    "Суми": 2,
    "Івано-Франківськ": 2,
    "Тернопіль": 1,
    "Рівне": 1,
    "Хмельницький": 1,
    "Кропивницький": 1,
    "Ужгород": 1,
    "Луцьк": 1,
    "Біла Церква": 1,
    "Краматорськ": 1,
    "Мелітополь": 1,
    "Бердянськ": 1,
    "Нікополь": 1
}
cities = list(city_population_share.keys())
city_weights = list(city_population_share.values())

# --- Генерація телефону ---
def generate_uk_phone():
    prefix = random.choice(["50", "66", "67", "68", "73", "91", "92", "93", "94", "95", "96", "97", "98", "99"])
    return f"+380{prefix}{random.randint(1000000, 9999999)}"

# --- Генерація користувачів ---
def generate_users(user_count):
    users = []
    for _ in range(user_count):
        gender = random.choice(["чоловік", "жінка"])
        first_name = random.choice(male_first_names if gender == "чоловік" else female_first_names)
        last_name = random.choice(male_last_names if gender == "чоловік" else female_last_names)
        city = random.choices(cities, weights=city_weights, k=1)[0]

        users.append({
            "Стать": gender,
            "Ім’я": first_name,
            "прізвище": last_name,
            "email": fake.email(),
            "Телефон": generate_uk_phone(),
            "Місто": city,
            "Адреса доставки": fake.address().replace("\n", ", ")
        })

    return users

salary_level_by_city = {
    "Київ": 1.3,
    "Харків": 1.1,
    "Одеса": 1.15,
    "Львів": 1.2,
    "Дніпро": 1.1,
    "Запоріжжя": 1.0,
    "Кривий Ріг": 0.95,
    "Миколаїв": 1.0,
    "Маріуполь": 0.9,
    "Вінниця": 1.0,
    "Херсон": 0.85,
    "Чернігів": 0.9,
    "Полтава": 0.95,
    "Черкаси": 1.0,
    "Житомир": 0.9,
    "Суми": 0.9,
    "Івано-Франківськ": 1.0,
    "Тернопіль": 0.95,
    "Рівне": 0.95,
    "Хмельницький": 0.95,
    "Кропивницький": 0.9,
    "Ужгород": 1.0,
    "Луцьк": 0.95,
    "Біла Церква": 0.9,
    "Краматорськ": 0.85,
    "Мелітополь": 0.85,
    "Бердянськ": 0.85,
    "Нікополь": 0.85
}

# --- Генерація замовлень ---
def generate_orders(users, min_percent=10, max_percent=20):
    total_buyers = random.randint(len(users) * min_percent // 100, len(users) * max_percent // 100)

    # Збираємо всі міста користувачів
    city_to_users = {}
    for user in users:
        city = user["Місто"]
        if city not in city_to_users:
            city_to_users[city] = []
        city_to_users[city].append(user)

    # Нормалізація ваг згідно з доступними користувачами
    available_cities = list(city_to_users.keys())
    available_weights = [city_population_share.get(city, 1) for city in available_cities]

    # Вибір міст покупців з урахуванням ваг
    selected_buyers = []
    while len(selected_buyers) < total_buyers:
        city = random.choices(available_cities, weights=available_weights, k=1)[0]
        if city_to_users[city]:
            selected_buyers.append(city_to_users[city].pop())  # Уникаємо повторень

    # Генерація замовлень
    data = []
    for user in selected_buyers:
        for _ in range(random.randint(1, 3)):
            product = random.choice(product_list)
            base_price = product_prices[product["назва"]]
            city_salary_factor = salary_level_by_city.get(user["Місто"], 1.0)
            price = int(base_price * city_salary_factor)
            discount = random.choices([0, 5, 10, 15], weights=[20, 30, 30, 20])[0]
            quantity = random.choices([1, 2], weights=[80, 20])[0] if discount == 0 else random.choices([1, 2, 3], weights=[50, 30, 20])[0]
            payment_method = random.choices(["картка", "онлайн", "післяплата", "готівка"], weights=[40, 30, 20, 10])[0]

            row = {
                "Дата замовлення": fake.date_between(start_date="-1y", end_date="today"),
                "ID замовлення": fake.uuid4(),
                **user,
                "Продукт": product["назва"],
                "Категорія товару": product["категорія"],
                "Кількість": quantity,
                "Ціна за одиницю": price,
                "Знижка (%)": discount,
                "Метод оплати": payment_method,
                "Служба доставки": random.choice(["Нова Пошта", "Укрпошта", "Meest", "Самовивіз"]),
                "Статус доставки": random.choice(["Очікує", "Відправлено", "Доставлено", "Скасовано"]),
                "Сума": round(quantity * price * (1 - discount / 100), 2)
            }
            data.append(row)

    return pd.DataFrame(data)


# --- Генерація та збереження ---
users = generate_users(8931)
df = generate_orders(users, min_percent=10, max_percent=20)
df.to_excel("detailed_sales_data.xlsx", index=False)
print(f"✅ Збережено {len(df)} рядків у detailed_sales_data.xlsx")
