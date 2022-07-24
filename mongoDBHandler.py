import pymongo
from pymongo import MongoClient
import json
import dns.resolver
from jsonHandler import *
import pprint

dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8'] # this is a google public dns server,  use whatever dns server you like here

client = pymongo.MongoClient("mongodb+srv://velocity300:vELOcity300@elo.r5j0e.mongodb.net/?retryWrites=true&w=majority&ssl=true")
db = client.vELOcity

def addDocumentMongo(dictionary, collectionName):
    target = db[collectionName]
    for elem in dictionary:
        result = target.insert_one(elem)

def countInstancesMongo(key, value, collectionName):
    target = db[collectionName]
    query = {key:value}
    return target.count_documents(query)
    
def getKillsMongo(valorantName):
    target = db['gamesData']
    result = (target.aggregate([
            {
                "$unwind": "$kills"
            },
            { 
                "$group": {
                    "_id": "$kills.killer_display_name", "total": {"$sum":1}
                }
            }
    ]))
    for elem in result:
        if elem["_id"] == valorantName:
            return elem
        else:
            return None



