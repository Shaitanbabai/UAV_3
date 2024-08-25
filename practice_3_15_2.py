import time
import math

def slow_function():
    result = 0
    for i in range(1, 1000000):
        result += math.sqrt(i)
    return result

if __name__ == '__main__':
    print("start")
    time.sleep(10)
    slow_function()
    print("stop")