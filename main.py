import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.template_filter('enumerate_items')
def enumerate_items(iterable, start=0):
    return enumerate(iterable, start=start)


def load_items():
    with open("foods.json", "r") as f:  # Replace "your_items.json" with your actual JSON file name
        data = json.load(f)
        return data["items"]


def save_items(items):
    with open("foods.json", "w") as f:  # Replace "your_items.json" with your actual JSON file name
        json.dump({"items": items}, f, indent=4)


@app.route("/", methods=["GET"])
def show_items():
    items = load_items()
    print(items)
    total_calories = sum(item["calories"] for item in items)
    return render_template("index.html", items=items, total_calories=total_calories)


@app.route("/", methods=["POST"])
def process_form():
    items = load_items()
    total_calories = sum(item["calories"] for item in items)

    if "remove_item" in request.form:
        index = int(request.form.get("remove_item"))
        if index >= 0 and index < len(items):
            total_calories -= items[index]["calories"]
            del items[index]
            save_items(items)
    else:
        new_item = request.form.get("new_item")
        calories = int(request.form.get("calories"))
        amount = int(request.form.get("amount"))
        total_calories = amount * calories  # This line calculates the total calories for the new item
        items.append({"foodname": new_item, "amount": amount, "calories": total_calories})
        save_items(items)
        total_calories += sum(item["calories"] for item in items)  # Sum up calories for all items

    return redirect(url_for("show_items"))  # Redirect to GET route to show updated list


if __name__ == "__main__":
    app.run(debug=True)
