from pymongo import MongoClient
import os

# Připojovací řetězec
uri = os.getenv("MONGODB_URL")
## uri = 'mongodb+srv://admin:admindb@footballmatchesdb.ywjx4tg.mongodb.net/?retryWrites=true&w=majority'

# Vytvoření klienta MongoDB
client = MongoClient(uri)

# Vytvoření nebo získání databáze z klienta
db = client["FootballDB"]
