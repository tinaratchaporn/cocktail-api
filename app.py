from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
from deep_translator import GoogleTranslator

app = Flask(__name__)
CORS(app)

# โหลดข้อมูล
with open("cocktails_combined.json", "r", encoding="utf-8") as f:
    cocktails = json.load(f)

# ฟังก์ชันแปลข้อความเป็นภาษาไทย
def translate(text):
    try:
        return GoogleTranslator(source='en', target='th').translate(text)
    except:
        return text

# แปลข้อมูลค็อกเทลทั้งเมนู
def translate_cocktail(cocktail):
    return {
        "id": cocktail["id"],
        "name": translate(cocktail["name"]),
        "category": translate(cocktail.get("category", "")),
        "alcohol_level": translate(cocktail.get("alcohol_level", "")),
        "tags": [translate(t) for t in cocktail.get("tags", [])],
        "ingredients": [
            {
                "name": translate(i["name"]),
                "measure": i.get("measure", "-")
            } for i in cocktail["ingredients"]
        ],
        "instructions": translate(cocktail["instructions"])
    }

@app.route("/")
def home():
    return jsonify({"message": "ยินดีต้อนรับสู่ Cocktail API (ภาษาไทย)"})

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

    # แปลแค่ชื่อ cocktail ที่โชว์เป็น list
    return jsonify([
        {"id": c["id"], "name": translate(c["name"])}
        for c in results[:5]
    ])

@app.route("/random", methods=["GET"])
def random_cocktail():
    c = random.choice(cocktails)
    return jsonify(translate_cocktail(c))

@app.route("/cocktail/<id>", methods=["GET"])
def get_cocktail(id):
    for c in cocktails:
        if str(c["id"]) == id:
            return jsonify(translate_cocktail(c))
    return jsonify({"error": "ไม่พบเมนู"}), 404

if __name__ == "__main__":
    app.run()
