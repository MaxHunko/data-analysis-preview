import pandas as pd
import plotly.express as px
import os

# === Створення папки для графіків ===
if not os.path.exists("graphs"):
    os.makedirs("graphs")
    print("📁 Створено папку 'graphs'")
else:
    print("📁 Папка 'graphs' вже існує")

# === Завантаження даних ===
print("📊 Завантаження даних із файлу...")
df = pd.read_excel("detailed_sales_data.xlsx")
df["Дата замовлення"] = pd.to_datetime(df["Дата замовлення"])
df["Місяць"] = df["Дата замовлення"].dt.to_period("M").astype(str)
df["Тиждень"] = df["Дата замовлення"].dt.to_period("W")
df["День"] = df["Дата замовлення"].dt.date
df["Користувач"] = df["Телефон"]
print("✅ Дані успішно завантажені\n")

# === Ключові метрики ===
dau = df.groupby("День")["Користувач"].nunique().mean().round(2)
wau = df.groupby("Тиждень")["Користувач"].nunique().mean().round(2)
mau = df.groupby("Місяць")["Користувач"].nunique().mean().round(2)
total_users = df["Користувач"].nunique()
repeat_users = df.groupby("Користувач").filter(lambda x: len(x) > 1)["Користувач"].nunique()
retention_rate = round((repeat_users / total_users) * 100, 2)
churn_rate = round(100 - retention_rate, 2)
ltv = df.groupby("Користувач")["Сума"].sum().mean().round(2)

# === HTML-блок з ключовими метриками ===
metrics_block = f"""
<div class="chart" style="width: 98%; padding:20px; border-radius:10px; font-size:18px; line-height:1.6">
    <h2 style="color:#00d4ff">📊 Ключові метрики продукту</h2>
    <ul style="list-style:none; padding:0">
        <li>🔸 <strong>DAU</strong> (на день): {dau}</li>
        <li>🔸 <strong>WAU</strong> (на тиждень): {wau}</li>
        <li>🔸 <strong>MAU</strong> (на місяць): {mau}</li>
        <li>🔁 <strong>Retention Rate</strong>: {retention_rate}%</li>
        <li>❌ <strong>Churn Rate</strong>: {churn_rate}%</li>
        <li>💰 <strong>LTV</strong> (середній дохід з клієнта): ₴{ltv}</li>
    </ul>
</div>
"""

# === Графіки ===
figures = []

print("📈 Топ-10 продаваних товарів...")
top_products = df["Продукт"].value_counts().nlargest(10).reset_index()
top_products.columns = ["Продукт", "Кількість"]
fig1 = px.bar(top_products, x="Продукт", y="Кількість", title="🔝 Топ-10 продаваних товарів", color="Кількість")
figures.append(fig1)

print("📈 Дохід по категоріях...")
rev_cat = df.groupby("Категорія товару")["Сума"].sum().reset_index().sort_values("Сума", ascending=False)
fig2 = px.bar(rev_cat, x="Категорія товару", y="Сума", title="💰 Дохід по категоріях", color="Сума")
figures.append(fig2)

print("📈 Середній чек по містах...")
avg_city = df.groupby("Місто")["Сума"].mean().sort_values(ascending=False).head(10).reset_index()
fig3 = px.bar(avg_city, x="Місто", y="Сума", title="🏙️ Середній чек по містах", color="Сума")
figures.append(fig3)

print("📈 Замовлення по місяцях...")
monthly = df.groupby("Місяць").size().reset_index(name="Кількість")
fig4 = px.line(monthly, x="Місяць", y="Кількість", title="📈 Замовлення по місяцях", markers=True)
figures.append(fig4)

print("📈 Вплив знижок на продажі...")
discount = df.groupby("Знижка (%)")["Сума"].sum().reset_index()
fig5 = px.bar(discount, x="Знижка (%)", y="Сума", title="🔻 Вплив знижок на продажі", color="Сума")
figures.append(fig5)

print("📈 Популярні способи оплати...")
payment = df["Метод оплати"].value_counts().reset_index()
payment.columns = ["Метод оплати", "Кількість"]
fig6 = px.pie(payment, names="Метод оплати", values="Кількість", title="💳 Популярні способи оплати")
figures.append(fig6)

print("📈 Кількість покупок по містах...")
city_orders = df["Місто"].value_counts().head(10).reset_index()
city_orders.columns = ["Місто", "Кількість"]
fig7 = px.bar(city_orders, x="Місто", y="Кількість", title="🏘️ Кількість покупок по містах", color="Кількість")
figures.append(fig7)

print("📈 Найпопулярніші товари по містах...")
city_product_counts = df.groupby(["Місто", "Продукт"]).size().reset_index(name="Кількість")
idx = city_product_counts.groupby("Місто")["Кількість"].idxmax()
top_products_by_city = city_product_counts.loc[idx].sort_values("Кількість", ascending=False)
fig8 = px.bar(top_products_by_city, x="Кількість", y="Місто", color="Продукт", orientation='h',
              title="🏆 Найпопулярніші товари в містах")
figures.append(fig8)

# === HTML з графіками ===
print("🧩 Об'єднання графіків в один HTML...")

html_blocks = []
for i, fig in enumerate(figures):
    div_id = f"plot{i}"
    fig_html = fig.to_html(full_html=False, include_plotlyjs='cdn', div_id=div_id)
    html_blocks.append(f'<div class="chart">{fig_html}</div>')

# === Завершення HTML ===
final_html = f"""
<html>
<head>
    <meta charset="utf-8">
    <title>Звіт з продажів</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            background: #f4f4f4;
            font-family: Arial;
        }}
        .container {{
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
        }}
        .chart {{
            width: 48%;
            margin: 10px 0;
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            padding: 10px;
        }}
    </style>
</head>
<body>
    <h1 style="text-align:center">📊 Звіт з продажів</h1>
    <div class="container">
        {metrics_block}
        {''.join(html_blocks)}
    </div>
</body>
</html>
"""

# === Збереження HTML ===
with open("graphs/all_graphs.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("✅ Усі графіки + метрики об'єднано в 'graphs/all_graphs.html'")
