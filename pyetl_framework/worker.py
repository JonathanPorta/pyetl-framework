import os
import redis
print("===============worker.py:3")
from rq import Queue, Connection
from rq import Worker as W

listen = ['default']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
print("===============worker.py:9")
conn = redis.from_url(redis_url)
print("===============worker.py:11")

class Worker():
    def run():
        print("===============worker.py:13")
        with Connection(conn):
            q = list(map(Queue, listen))
            print("===============worker.py:16", q)
            worker = W(q)
            worker.work()

if __name__ == '__main__':
    run()
