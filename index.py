from flask import Flask, request
import re

app = Flask(__name__)

point_transactions = []


def timestamp_to_seconds(timestamp):
    date_time_split = re.split(r"[-:TZ]", timestamp)

    year_diff = int(date_time_split[0]) - 2020
    year_diff_in_seconds = year_diff * 365 * 24 * 60 * 60

    month_diff = int(date_time_split[1]) - 1
    month_diff_in_seconds = month_diff * 30 * 24 * 60 * 60

    day_diff = int(date_time_split[2]) - 1
    day_diff_in_seconds = day_diff * 24 * 60 * 60

    hour_diff = int(date_time_split[3])
    hour_diff_in_seconds = hour_diff * 60 * 60

    minute_diff = int(date_time_split[4])
    minute_diff_in_seconds = minute_diff * 60

    second_diff = int(date_time_split[5])

    return (year_diff_in_seconds + month_diff_in_seconds + day_diff_in_seconds +
            hour_diff_in_seconds + minute_diff_in_seconds + second_diff)


@app.route("/add-points", methods=["POST"])
def add_points():
    transaction = request.json
    transaction_time = timestamp_to_seconds(transaction.timestamp)
    transaction.timestamp = transaction_time
    if len(point_transactions) == 0 or transaction_time > point_transactions[-1].timestamp:
        point_transactions.append(transaction)
        return

    inserted = False
    current_idx = 0
    while not inserted:
        pass
    return
