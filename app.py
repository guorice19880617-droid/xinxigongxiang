from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

# 初始化
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# =========================
# 客户页面
# =========================
@app.route("/client/<name>")
def client(name):
    data = load_data()
    return render_template("client.html", data=data.get(name, {}), name=name)

# =========================
# 后台
# =========================
@app.route("/admin", methods=["GET", "POST"])
def admin():

    data = load_data()

    if request.method == "POST":

        name = request.form["name"]

        data[name] = {
            "rate": request.form["rate"],
            "companies": {
                "海田": {
                    "margin": request.form["ht_margin"],
                    "payment": request.form["ht_payment"],
                    "address": request.form["ht_address"]
                },
                "大洲": {
                    "margin": request.form["dz_margin"],
                    "payment": request.form["dz_payment"],
                    "address": request.form["dz_address"]
                }
            }
        }

        save_data(data)
        return redirect("/admin")

    return render_template("admin.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
