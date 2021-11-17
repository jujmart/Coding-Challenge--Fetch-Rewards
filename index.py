from flask import Flask, request
import re
import json
import datetime

app = Flask(__name__)

point_transactions = []
balance = {}


def timestamp_conversion(timestamp):
    """
        Convert timestamp string to python-recognizeable timestamp to use for comparisons
    """
    date_time_split = re.split(r"[-:TZ]", timestamp)
    date = datetime.datetime(int(date_time_split[0]), int(date_time_split[1]), int(date_time_split[2]),
                             int(date_time_split[3]), int(date_time_split[4]), int(date_time_split[5]))
    return date


def timestamp_seconds_sorting(transaction):
    """
        Sort transactions based on their timestamp
    """
    return transaction["timestamp"]


@app.route("/add-points", methods=["POST"])
def add_points():
    """
        Route for adding points
    """
    transaction = request.json

    # Convert timestamp to python timestamp for comparisons
    transaction_time = timestamp_conversion(transaction["timestamp"])
    transaction["timestamp"] = transaction_time

    # Add transaction to array to be sorted later
    point_transactions.append(transaction)

    # Updating or adding new running balance for each payer
    if balance.get(transaction["payer"]):
        balance[transaction["payer"]] += transaction["points"]
    else:
        balance[transaction["payer"]] = transaction["points"]

    # Payer balance cannot be below 0
    balance[transaction["payer"]] = max(balance[transaction["payer"]], 0)

    # Return out of the function if transactions are already sorted in chronological order by timestamp
    if len(point_transactions) <= 1 or transaction_time >= point_transactions[-2]["timestamp"]:
        return {}

    # Sort transactions in chronological order by timestamp
    point_transactions.sort(key=timestamp_seconds_sorting)
    return {}


@app.route("/spend-points", methods=["POST"])
def spend_points():
    """
        Route for spending points
    """
    desired_points = request.json["points"]
    total_points = 0
    payer_lst = []
    current_idx = 0

    # Stop once we have deducted the desired points
    while total_points < desired_points:
        # Break for if we have reached the end of the list
        if current_idx >= len(point_transactions):
            break
        print(point_transactions)
        # Saving transaction we are currently looking at
        current = point_transactions[current_idx]

        # We will not need to worry about deducting negative points from the total
        if current["points"] < 0:
            current_idx += 1
            continue

        # For-loop to find if there are any negative points assessed so that they are not taken into account
        negative_points = 0
        for i in range(len(point_transactions)):
            if point_transactions[i]["payer"] != current["payer"] or point_transactions[i]["points"] > 0:
                continue

            negative_points -= point_transactions[i]["points"]

        # For-loop to find if there are any positive points assessed before the current transaction so that they are not taken into account when subtracting negative points
        positive_points = 0
        for i in range(current_idx):
            if point_transactions[i]["payer"] != current["payer"] or point_transactions[i]["points"] < 0:
                continue

            positive_points += point_transactions[i]["points"]

        point_diff = max(negative_points - positive_points, 0)

        # If there are points left in the current transaction after the negative points are taken into account, then we can post a negative transaction, update the balance, and increase our point deduction total
        if current["points"] >= point_diff:
            # Remaining points to spend could be the minimum of the points left that havent already been spent or the points left to spend out of the total from the request
            remaining_points = min(
                current["points"] - point_diff, desired_points - total_points)
            # Add a transaction that shows the amount spent by payer with the current time as a timestamp
            point_transactions.append({
                "payer": current["payer"],
                "points": -remaining_points,
                "timestamp": datetime.datetime.now()
            })
            # Add the amount to the payer list
            payer_lst.append({
                "payer": current["payer"],
                "points": -remaining_points
            })
            # Update the balance
            balance[current["payer"]] -= remaining_points
            # Update the total points spent so far
            total_points += remaining_points
            # move the current index
            current_idx += 1
            continue

    # Ensure the transactions are sorted
    point_transactions.sort(key=timestamp_seconds_sorting)
    return json.dumps(payer_lst)


@app.route("/points-balance")
def points_balance():
    """
        Route to return the running balance
    """
    return balance
