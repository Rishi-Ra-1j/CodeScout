import time
import httpx

URL = "https://generativelanguage.googleapis.com"

start = time.perf_counter()
httpx.get(URL, timeout=30)
print("new connection:", round((time.perf_counter() - start) * 1000), "ms")

with httpx.Client() as client:
    for i in range(3):
        start = time.perf_counter()
        client.get(URL, timeout=30)
        print("reused connection", i + 1, ":", round((time.perf_counter() - start) * 1000), "ms")