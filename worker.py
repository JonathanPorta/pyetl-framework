import os
import redis
print("===============worker.py:3")
from rq import Worker, Queue, Connection

listen = ['default']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
print("===============worker.py:9")
conn = redis.from_url(redis_url)
print("===============worker.py:11")
if __name__ == '__main__':
    print("===============worker.py:13")
    with Connection(conn):
        q = list(map(Queue, listen))
        print("===============worker.py:16", q)
        worker = Worker(q)
        worker.work()
