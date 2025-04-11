
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)

# Load cocktail data from JSON
with open("cocktails_combined.json", "r", encoding="utf-8") as f:
    cocktails = json.load(f)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to Cocktail API!"})

@app.route("/cocktails", methods=["GET"])
def search_cocktails():
    ingredient = request.args.get("ingredient")
    mood = request.args.get("mood")
    alcohol = request.args.get("alcohol_level")

    results = cocktails
    if ingredient:
        results = [c for c in results if any(ingredient.lower() in i["name"].lower() for i in c["ingredients"])]
    if mood:
        results = [c for c in results if mood.lower() in [t.lower() for t in c.get("tags", [])]]
    if alcohol:
        results = [c for c in results if alcohol.lower() in c.get("alcohol_level", "").lower()]

    return jsonify(results)

@app.route("/random", methods=["GET"])
def random_cocktail():
    return jsonify(random.choice(cocktails))

@app.route("/cocktail/<id>", methods=["GET"])
def get_cocktail(id):
    for c in cocktails:
        if str(c["id"]) == id:
            return jsonify(c)
    return jsonify({"error": "Cocktail not found"}), 404

if __name__ == "__main__":
    app.run()
