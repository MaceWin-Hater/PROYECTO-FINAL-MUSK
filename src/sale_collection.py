from src.sale import Sale
class SalesCollection:
    def __init__(self, sales):
        self.sales = sales

    def sales_by_client(self, client_id):
        result = []

        for sale in self.sales:
            if sale.client_id == client_id:
                result.append(sale)

        return result

    def total_amount_by_client(self, client_id):
        total = 0

        for sale in self.sales:
            if sale.client_id == client_id:
                total += sale.amount

        return total
