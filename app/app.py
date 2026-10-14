import os, redis
from flask import Flask

app = Flask(__name__)
r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379)
VERSION = os.getenv("APP_VERSION", "v1")

@app.get("/")
def index(): return f"ShopLite {VERSION} - e2e test"

@app.get("/health")
def health(): return "ok"

@app.get("/visits")
def visits(): return str(r.incr("visits"))
