from functools import reduce


def filter_sales_by_category(sales, category):
    return list(filter(lambda s: s.category == category, sales))


def filter_sales_by_client(sales, client_id):
    return list(filter(lambda s: s.client_id == client_id, sales))


def sum_amounts(sales):
    return reduce(lambda total, s: total + s.amount, sales, 0)


def client_with_most_sales_in_category(clients, sales, category):
    category_sales = filter_sales_by_category(sales, category)

    counts = {}
    for sale in category_sales:
        counts[sale.client_id] = counts.get(sale.client_id, 0) + 1

    if not counts:
        return None

    top_client_id = max(counts, key=counts.get)

    for client in clients:
        if client.client_id == top_client_id:
            return client.name

    return None
