import pymongo
import certifi


con_str = "mongodb+srv://xyr10:testPassword1234@cluster0.cx0a1zz.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())
db = client.get_database('mymerch')
