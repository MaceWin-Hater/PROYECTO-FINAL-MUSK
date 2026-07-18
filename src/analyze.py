import json
import csv

def generate_report():
  with open("data/clients.json", "r") as file:
    clients = json.load(file)
