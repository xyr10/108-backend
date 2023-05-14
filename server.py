from flask import Flask, request, abort
import json
from config import db
from flask_cors import CORS
from bson import ObjectId

app = Flask(__name__)
CORS(app)  # disable CORS security rule


@app.get("/")
def home():
    return "Hello from Flask"


@app.get("/test")
def test():
    return "This is another page"

### API ENDPOINTS ####
### JSON  ############


def fix_id(obj):
    # fix the object to be json parsable
    obj["_id"] = str(obj["_id"])
    return obj


@app.get("/api/about")
def about():
    me = {"name": "Xyrone Ocampo"}
    return json.dumps(me)


@app.get("/api/catalog")
def get_catalog():
    products = []
    cursor = db.products.find({})
    for prod in cursor:
        products.append(fix_id(prod))

    return json.dumps(products)


@app.post("/api/catalog")
def save_product():
    data = request.get_json()

# apply validation
# BR1: Title must exist and should have at least 6 char
    if "title" not in data or len(data["title"]) < 6:
        return abort(400, "Invalid Title")

# BR2: There must be a price, and should be greater than zero
    if "price" not in data or data["price"] <= 0:
        return abort(400, "Invalid price")

# BR3: there must be a category
    if "category" not in data:
        return abort(400, "Invalid category")

    db.products.insert_one(data)
    return json.dumps(fix_id(data))  # will fail


# get /api/total
# return the total value of your catalog (the sum of all prices)


@app.get("/api/total")
def total_value():

    cursor = db.products.find({})
    total = 0
    for prod in cursor:
        total += prod["price"]

    return json.dumps(total)

    # get /api/products
    # # return the number of products in the catalog


@app.get("/api/products")
def number_products():

    cursor = db.products.find({})
    count = 0
    for prod in cursor:
        count += 1
        ["products"]

    return json.dumps(count)

# get /api/products
# # return the number of products in the catalog


@app.get("/api/products")
def count_products():
    cursor = db.products.find({})
    count = 0
    for prod in cursor:
        count += 1

    return json.dumps(count)


# get /api/categories
# should return the list of categories
# retrieve all products, get the category and put it on a list
# return the list as json

@app.get("/api/categories")
def get_categories():
    categories = []
    cursor = db.products.find({})
    for prod in cursor:
        cat = prod["category"]
        if cat not in categories:
            categories.append(cat)

    return json.dumps(categories)


# /api/products/category/A
# /api/products/category/X
# /api/products/category/T
# /api/products/category/T/Something


@app.get("/api/products/category/<name>")
def get_by_category(name):
    results = []
    cursor = db.products.find({})
    for prod in cursor:
        if (prod["category"] == name)

    return json.dumps(results)


@app.get("/api/products/category/<name>")
def get_by_category(name):
    results = []
    cursor = db.products.find({"category:name"})
    for prod in cursor:
        if (prod["category"] == name)

    return json.dumps(results)

# get /api/products/search/test


@app.get("/api/products/search/<term>")
def search_products(term):
    results = []
    cursor = db.products.find({"title": {"$regex": term, "$options": "i"}})
    for prod in cursor:
        results.append(fix_id(prod))

    return json.dumps(results)

# get /api/products/lower/value
# to retrieve all products whose price is lower than given value
# go to google, search "pymongo lower than operator" then choose the most recent answer (some may be old)


@app.get("/api/products/lower/<value>")
def price_lower(value):
    results = []
    cursor = db.products.find({"price": {"$lt": float(value)}})
    for prod in cursor:
        results.append(fix_id(prod))

    return json.dumps(results)

    # app.run(debug=True)


# get /api/products/greater/value
# greater than or equal
# to retrieve all products whose price is lower than given value

@app.get("/api/products/greater/<value>")
def price_greater(value):
    results = []
    cursor = db.products.find({"price": {"$gte": float(value)}})
    for prod in cursor:
        results.append(fix_id(prod))

    return json.dumps(results)


@app.delete("/api/products/<title>")
def delete_product(title):
    db.products.delete_one({"title": title})
    return json.dumps({"status": "OK", "message": "Product Deleted"})


@app.delete("/api/products/byid/<id>")
def delete_by_id(id):
    db_id = ObjectId(id)
    db.products.delete_one({"_id": db_id})
    return json.dumps({"status": "OK", "message": "Product Deleted"})
#
# ##### COUPON CODES ##########
#

# get /api/coupons -> retrieve all


@app.get("/api/coupons")
def get_coupons():
    results = []
    cursor = db.coupons.find({})
    for coupon in cursor:
        results.append(fix_id(coupon))

    return json.dumps(results)

# post /api/coupons -> save new


@app.post("/api/coupons")
def save_coupons():
    data = request.get_json()

# code must exist
# should have at least 5 char
    if not "code" in data or len(data["code"]) < 5:
        return abort(400, "Invalid code")

    # the code should be unique (?)
    existing = db.coupons.find_one({"code": data["code"]})
    if existing:
        return abort(400, "Error: code already exists ont he list of couponse")

# discount should exist
# should be greater than 5 and less than 40%
    if "discount" not in data:
        return abort(400, "Invalid discount")

    # discount its a number (int or a float)
    if not isinstance(data["discount"], (int, float)):
        return abort(400, "Invalid price, must be an int or a float")

    if data["discount"] < 5 or data["discount"] > 40:
        return abort(400, "Invalid discount, should be between 5 and 40")

    db.coupons.insert_one(data)

    return json.dumps(fix-id(data))


# GET /api/coupons/<code> -> retrieve 1 by code

@app.get("/api/coupons/<code>")
def coupon_by_code(code):
    coupon = db.coupons.find_one({"code": code})
    if not coupon:
        return abort(404, "Invalid Code")

    return json.dumps(fix_id(coupon))


@app.delete("/api/coupons/<code>")
def delete_coupon(code):
    db.coupons.delete_one({"code": code})
    return json.dumps({"status": "OK", "message": "Coupon Deleted"})
