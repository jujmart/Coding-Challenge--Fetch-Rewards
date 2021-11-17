from flask import Flask, request
import re
import json
import datetime

app = Flask(__name__)

point_transactions = []
balance = {}


def timestamp_conversion(timestamp):
    date_time_split = re.split(r"[-:TZ]", timestamp)
    date = datetime.datetime(int(date_time_split[0]), int(date_time_split[1]), int(date_time_split[2]),
                             int(date_time_split[3]), int(date_time_split[4]), int(date_time_split[5]))
    return date


def timestamp_seconds_sorting(transaction):
    return transaction["timestamp"]


@app.route("/add-points", methods=["POST"])
def add_points():
    transaction = request.json
    transaction_time = timestamp_conversion(transaction["timestamp"])
    transaction["timestamp"] = transaction_time
    point_transactions.append(transaction)

    if balance.get(transaction["payer"]):
        balance[transaction["payer"]] += transaction["points"]
    else:
        balance[transaction["payer"]] = transaction["points"]

    balance[transaction["payer"]] = max(balance[transaction["payer"]], 0)

    if len(point_transactions) <= 1 or transaction_time >= point_transactions[-2]["timestamp"]:
        print(point_transactions)
        print("**********************")
        print(balance)
        return {}

    point_transactions.sort(key=timestamp_seconds_sorting)
    print(point_transactions)
    print("**********************")
    print(balance)
    return {}


@app.route("/spend-points", methods=["POST"])
def spend_points():
    desired_points = request.json["points"]
    total_points = 0
    payer_lst = []
    current_idx = 0

    while total_points < desired_points:
        if current_idx >= len(point_transactions):
            break

        current = point_transactions[current_idx]

        if current["points"] < 0:
            current_idx += 1
            continue

        negative_points = 0
        for i in range(current_idx + 1, len(point_transactions)):
            if point_transactions[i]["payer"] != current["payer"] or point_transactions[i]["points"] > 0:
                continue

            negative_points += point_transactions[i]["points"]

        if current["points"] >= negative_points:
            remaining_points = min(
                current["points"] + negative_points, desired_points - total_points)
            point_transactions.append({
                "payer": current["payer"],
                "points": -remaining_points,
                "timestamp": datetime.datetime.now()
            })
            payer_lst.append({
                "payer": current["payer"],
                "points": -remaining_points
            })
            balance[current["payer"]] -= remaining_points
            total_points += remaining_points
            current_idx += 1
            continue

    point_transactions.sort(key=timestamp_seconds_sorting)
    print(point_transactions)
    print("**********************")
    print(balance)
    return json.dumps(payer_lst)


@app.route("/points-balance")
def points_balance():
    return balance
