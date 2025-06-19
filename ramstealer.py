import time
import sys
import psutil
from threading import Thread
import random

def memory_hog(size_mb):
    try:
        data = bytearray(random.randbytes(1024 * 1024 * size_mb))
        while True:
            _ = sum([x * x for x in range(10000)])
            time.sleep(random.uniform(0.01, 0.05))
    except MemoryError:
        print("Memory allocation failed for thread, continuing...")
        return
    except Exception as e:
        print(f"Thread error: {e}")
        return

if __name__ == "__main__":
    print("starting ctrl+c to stop")
    threads = []
    total_mb = int(psutil.virtual_memory().available / (1024 * 1024) * 0.9)
    thread_count = max(1, total_mb // 180)
    print(f"attempting to allocate ~{thread_count * 220} MB across ~{thread_count} threads...")

    try:
        for i in range(thread_count):
            t = Thread(target=memory_hog, args=(220,))
            t.daemon = True
            t.start()
            threads.append(t)
            time.sleep(0.05)
            print(f"thread began {i+1}/{thread_count}")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("stopping...")
        sys.exit(0)
    except Exception as e:
        print(f"error: {e}")
        sys.exit(1)