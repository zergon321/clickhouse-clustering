from clickhouse_driver import Client
from datetime import datetime

if __name__ == "__main__":
    client = Client("127.0.0.1", port="9003")

    client.execute("CREATE DATABASE IF NOT EXISTS db")

    client.execute('''CREATE TABLE IF NOT EXISTS db.entries(
                      timestamp DateTime,
                      parameter String,
                      value Float64)
                      ENGINE = MergeTree()
                      PARTITION BY parameter
                      ORDER BY timestamp''')

    client.execute("INSERT INTO db.entries (timestamp, parameter, value) VALUES", \
        [(datetime.utcnow(), "elasticity", 38.9), (datetime.utcnow(), "gravity", 27.2), \
            (datetime.utcnow(), "density", 19.8)])
    
    data = client.execute("SELECT * FROM db.entries")

    for row in data:
        print("Timestamp", row[0], sep=": ")
        print("Parameter", row[1], sep=": ")
        print("Value", row[2], sep=": ")
        print()