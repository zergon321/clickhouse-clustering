from clickhouse_driver import Client

subs = [
    ("127.0.0.1", "9001"),
    ("127.0.0.1", "9002"),
    ("127.0.0.1", "9003")
]
master = ("127.0.0.1", "9000")

if __name__ == "__main__":
    for sub in subs:
        client = Client(sub[0], port=sub[1])

        client.execute("CREATE DATABASE IF NOT EXISTS db")

        client.execute('''CREATE TABLE IF NOT EXISTS db.entries(
                          timestamp DateTime,
                          parameter String,
                          value Float64)
                          ENGINE = MergeTree()
                          PARTITION BY parameter
                          ORDER BY (timestamp, parameter)''')
    
    client = Client(master[0], port=master[1])

    client.execute("CREATE DATABASE IF NOT EXISTS db")

    client.execute('''CREATE TABLE IF NOT EXISTS db.entries(
                      timestamp DateTime,
                      parameter String,
                      value Float64)
                      ENGINE = Distributed(example_cluster, db, entries, rand())''')
