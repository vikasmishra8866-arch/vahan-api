import requests
from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder="templates")
CORS(app)  # Mobile aur Browser blocking se bachane ke liye


# 1. Main Website Route
@app.route("/")
def home():
    return render_template("index.html")


# 2. Vahan API Route (Jo index.html se `/api/vahan/NUM` call ho raha hai)
@app.route("/api/vahan/<reg_no>")
def get_vahan_details(reg_no):
    try:
        # Vahan API se data fetch karna
        url = f"https://cjpindia.vercel.app/api/vehicle-details/{reg_no}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        # Python server se request ja rahi hai (Isme CORS Block nahi hota)
        response = requests.get(url, headers=headers, timeout=20)

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return (
                jsonify(
                    {"error": "Vehicle not found or upstream server error"}
                ),
                404,
            )

    except Exception as e:
        print("Backend Error:", e)
        return (
            jsonify(
                {"error": "Failed to fetch details", "details": str(e)}
            ),
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
