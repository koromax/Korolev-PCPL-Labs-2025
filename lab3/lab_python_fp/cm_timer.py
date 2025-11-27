import time
from contextlib import contextmanager

class cm_timer_1:
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"time: {time.time() - self.start_time}")

@contextmanager
def cm_timer_2():
    start_time = time.time()

    try:
        yield start_time
    finally:
        print(f"time: {time.time() - start_time}")

if __name__ == "__main__":
    with cm_timer_1():
        time.sleep(1.5)
    with cm_timer_2():
        time.sleep(1.5)
