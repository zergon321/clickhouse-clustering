from clickhouse_driver import Client
from datetime import datetime

if __name__ == "__main__":
    client = Client("127.0.0.1", port="9002")

    client.execute("CREATE DATABASE IF NOT EXISTS db")

    client.execute('''CREATE TABLE IF NOT EXISTS db.entries(
                      timestamp DateTime,
                      parameter String,
                      value Float64)
                      ENGINE = MergeTree()
                      PARTITION BY parameter
                      ORDER BY timestamp''')

    client.execute("INSERT INTO db.entries (timestamp, parameter, value) VALUES", \
        [(datetime.utcnow(), "voltage", 72.8), (datetime.utcnow(), "humidity", 39.8), \
            (datetime.utcnow(), "temperature", 88.13)])
    
    data = client.execute("SELECT * FROM db.entries")

    for row in data:
        print("Timestamp", row[0], sep=": ")
        print("Parameter", row[1], sep=": ")
        print("Value", row[2], sep=": ")
        print()