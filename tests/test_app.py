import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
import app as shop

class FakeRedis:
    def __init__(self): self.n = 0
    def incr(self, k): self.n += 1; return self.n
    def ping(self): return True

def test_health():
    c = shop.app.test_client()
    assert c.get("/health").status_code == 200

def test_index():
    c = shop.app.test_client()
    assert b"ShopLite" in c.get("/").data
