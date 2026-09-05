import json
import os

import pandas as pd

from src.client import Client
from src.sale import Sale
from src.client_collection import ClientCollection
from src.sales_collection import SalesCollection
from src.functional_utils import client_with_most_sales_in_category

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENTS_PATH = os.path.join(BASE_DIR, "data", "clients.json")
SALES_PATH = os.path.join(BASE_DIR, "data", "sales.csv")

HIGH_SPENDING_THRESHOLD = 500


def load_clients(path=CLIENTS_PATH):
    with open(path, "r", encoding="utf-8") as f:
        raw_clients = json.load(f)
    return [Client(**c) for c in raw_clients]


def load_sales(path=SALES_PATH):
    df = pd.read_csv(path)
    sales = []
    for _, row in df.iterrows():
        sales.append(Sale(
            sale_id=row["sale_id"],
            client_id=int(row["client_id"]),
            product=row["product"],
            category=row["category"],
            amount=float(row["amount"]),
            date=row["date"],
        ))
    return sales, df


def generate_report():
    clients = load_clients()
    sales, sales_df = load_sales()

    client_collection = ClientCollection(clients)
    sales_collection = SalesCollection(sales)

    # Cálculo 1) Número total de clientes
    total_clients = len(clients)

    # Cálculo 2) Número total de ventas
    total_sales = len(sales)

    # Cálculos 3, 4, 5) Por cliente: total gastado, número de ventas, promedio
    clients_report = []
    for client in clients:
        total_spent = sales_collection.total_amount_by_client(client.client_id)
        sale_count = len(sales_collection.sales_by_client(client.client_id))
        average_sale = round(total_spent / sale_count, 2) if sale_count else 0

        clients_report.append({
            "client_id": client.client_id,
            "name": client.name,
            "total_spent": total_spent,
            "sale_count": sale_count,
            "average_sale": average_sale,
        })

    total_revenue = sum(s.amount for s in sales)

    # Cálculo 6) Cliente con mayor gasto por país
    top_client_by_country = {}
    countries = sorted(set(c.country for c in clients))
    for country in countries:
        country_clients = client_collection.clients_by_country(country)
        top_client = max(
            country_clients,
            key=lambda c: sales_collection.total_amount_by_client(c.client_id),
        )
        top_client_by_country[country] = top_client.name

    # Cálculo 7) Total de ventas por categoría (pandas)
    category_totals = sales_df.groupby("category")["amount"].sum()
    sales_by_category = {k: float(v) for k, v in category_totals.items()}

    # Cálculo 8) Cliente con más ventas en una categoría específica
    top_electronics_client = client_with_most_sales_in_category(clients, sales, "Electronics")

    # Cálculo 9) Clientes con gasto alto
    high_spending_clients = [
        c["name"] for c in clients_report if c["total_spent"] > HIGH_SPENDING_THRESHOLD
    ]

    # Cálculo 10) Ventas acumuladas mes a mes
    sales_df["date"] = pd.to_datetime(sales_df["date"])
    sales_df["month"] = sales_df["date"].dt.to_period("M").astype(str)
    monthly_totals = sales_df.groupby("month")["amount"].sum()
    monthly_sales = {k: float(v) for k, v in monthly_totals.items()}

    return {
        "summary": {
            "total_clients": total_clients,
            "total_sales": total_sales,
            "total_revenue": total_revenue,
        },
        "clients": clients_report,
        "top_client_by_country": top_client_by_country,
        "top_client_electronics": top_electronics_client,
        "sales_by_category": sales_by_category,
        "high_spending_clients": high_spending_clients,
        "monthly_sales": monthly_sales,
    }


if __name__ == "__main__":
    report = generate_report()
    output_path = os.path.join(BASE_DIR, "report.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"Informe generado en {output_path}")
