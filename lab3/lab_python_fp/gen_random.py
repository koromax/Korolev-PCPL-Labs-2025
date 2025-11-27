import random

def gen_random(n, min, max):
    return [random.randint(min, max) for i in range(n)]

if __name__ == "__main__":
    print(*gen_random(10, 1, 10))
