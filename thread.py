import concurrent.futures
import requests
import threading
import time


# This example uses threading

"""
The thread local storage  (threading.local()), creates an object that looks like a global but is specific to each individual thread.
In this case, we've created a session for each thread
"""
# Initializing thread local storage
thread_local = threading.local()


def get_session():
    """
    Checks if the thread local storage has an attribute called session and if it doesn't, it adds the request session to it then returns the session.
    -> When get_session() is called, the session it looks up is specific to the particular thread on which it is running. Each thread will create a single session the first time it calls get_session() and then will simply use that session on each subsequent call throughout its lifetime
    """
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    session = get_session()
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")


def download_all_sites(sites):
    # if you go any higher than 10 threads, the extra overhead of creating and destroying the threads erases any time savings
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_site, sites)


if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")