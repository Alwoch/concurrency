# Race conditions in threading

import concurrent.futures

"""
In this code, each of the threads is accessing the same global variable counter and incrementing it. Counter is not protected in any way so it is not thread safe

-> Inorder to increment counter, each of the threads needs to read the current value and add one to it and save that value vack to he variable
"""

counter = 0


def increment_counter(fake_value):
    global counter
    for _ in range(100):
        counter += 1


if __name__ == "__main__":
    fake_data = [x for x in range(5000)]
    counter = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=5000) as executor:
        executor.map(increment_counter, fake_data)