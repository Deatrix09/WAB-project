from pymongo import MongoClient

# Připojovací řetězec
uri = "mongodb+srv://admin:admindb@footballmatchesdb.ywjx4tg.mongodb.net/?retryWrites=true&w=majority"

# Vytvoření klienta MongoDB
client = MongoClient(uri)

# Vytvoření nebo získání databáze z klienta
db = client["FootballDB"]
