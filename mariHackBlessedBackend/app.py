from flask import Flask
from flask_pymongo import PyMongo
from apscheduler.schedulers.background import BackgroundScheduler
import requests

from datetime import datetime, timedelta

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/bankHack"
mongo = PyMongo(app)

def computeBrokerIndex():
    


    return 1



incrementedTime = 0

def fetch_data_and_store():
    global incrementedTime
    incrementedTime += 2

    original_time_str = "2020-01-30 09:30:00.010000000"

    datetime_part_str, nanosecond_part_str = original_time_str.split(".")

    datetime_part = datetime.strptime(datetime_part_str, "%Y-%m-%d %H:%M:%S")

    incremented_datetime1 = datetime_part + timedelta(seconds=incrementedTime)
    incremented_datetime2 = datetime_part + timedelta(seconds=incrementedTime+3)

    incremented_datetime_str1 = incremented_datetime1.strftime("%Y-%m-%d %H:%M:%S")
    incremented_datetime_str2 = incremented_datetime2.strftime("%Y-%m-%d %H:%M:%S")

    incremented_time_str1 = f"{incremented_datetime_str1}.{nanosecond_part_str}"
    incremented_time_str2 = f"{incremented_datetime_str2}.{nanosecond_part_str}"

    print(incremented_time_str1, incremented_time_str2)

    data_cursor = mongo.db.bankHack_mock.find({
        "time": {"$gte": incremented_time_str1, "$lt": incremented_time_str2}
    })

    data_list = list(data_cursor)

    # Check if there are documents to transfer
    if data_list:
        # Prepare documents for insertion (e.g., remove existing '_id' to avoid duplication errors)
        for data in data_list:
            data.pop('_id', None)  # Remove '_id' if it exists to avoid insert duplication error

        # Insert documents into the target collection
        result = mongo.db.bankHackData.insert_many(data_list)

        print(f"Transferred {len(result.inserted_ids)} documents to bankHackData.")
    else:
        print("No documents found to transfer.")



@app.route('/getBrokerIndex')
def getBrokerIndexById():
    return 'Hello, World!'


@app.route('/getTopBrokers')
def getTopBrokers():
    return 'Hello, World!'

@app.route('/getRecentTrades')
def getRecentTrades():
    return 'Hello, World!'




@app.route('/getBrokerIndexPlot')
def getBrokerIndexPlot():
    return 'Hello, World!'


@app.route('/getBrokerIndexPlot')
def hello_world():
    return 'Hello, World!'


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(fetch_data_and_store, 'interval', seconds=2)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)
