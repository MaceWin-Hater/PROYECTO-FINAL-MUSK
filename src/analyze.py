import json
import csv

def generate_report():
  with open("data/clients.json", "r") as file:
    clients = json.load(file)

  sales = []
  with open("data/sales.csv", "r") as file:
    reader = csv.DictReader(file)
    
    for row in reader:
      sales.append(row)

  report = {
    "summary": {
      "total_clients": len(clients),
      "total_sales": len(sales),
      "total_revenue": 0
    }
  }
  return report
