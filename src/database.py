from pymongo import MongoClient
import os

# Připojovací řetězec
uri = os.getenv("MONGODB_URL")

# Vytvoření klienta MongoDB
client = MongoClient(uri)

# Vytvoření nebo získání databáze z klienta
db = client["FootballDB"]
