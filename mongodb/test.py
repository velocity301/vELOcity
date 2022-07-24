import pymongo
from pymongo import MongoClient
import json
import dns.resolver

dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8'] # this is a google public dns server,  use whatever dns server you like here

client = pymongo.MongoClient("mongodb+srv://velocity300:vELOcity300@elo.r5j0e.mongodb.net/?retryWrites=true&w=majority&ssl=true")

db = client.vELOcity
with open("players.json") as f:
    fileData = json.load(f)

for elem in fileData:
    result = db.players.insert_one(elem)