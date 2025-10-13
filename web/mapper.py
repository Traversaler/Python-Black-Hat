# 扫描wordpress常见文件和目录
import contextlib
import os
import queue
import requests
import sys
import threading
import time


FILTERED = [".jpg", ".gif", ".png", ".css"]
TARGET = "http://boodelyboo.com/wordpress"
THREADS = 10

# 存储实际扫描的路径
answers = queue.Queue()
# 存储准备扫描的路径
web_paths = queue.Queue()


def gather_paths():
    for root, _, files in os.walk('.'):
        for fname in files:
            if os.path.splitext(fname)[1] in FILTERED:
                continue
            path = os.path.join(root, fname)
            if path.startswith('.'):
                path = path[1:]
            print(path)
            web_paths.put(path)


def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = f'{TARGET}{path}'
        # 目标可能有节流或锁定
        time.sleep(2)
        r = requests.get(url)
        if r.status_code == 200:
            answers.put(url)
            sys.stdout.write('+')
        else:
            sys.stdout.write('x')
        sys.stdout.flush()


def run():
    mythreads = list()
    for i in range(THREADS):
        print(f'Spawning thread {i}')
        t = threading.Thread(target=test_remote())
        mythreads.append(t)
        t.start()

    for thread in mythreads:
        thread.join()


@contextlib.contextmanager
# chdir函数能在另一个目录下执行代码，保证在退出时回到原本目录
def chdir(path):
    """
    进入，改变目录为指定路径
    退出，改变目录回到初始
    """
    this_dir = os.getcwd()
    os.chdir(path)
    try:
        # 将控制权移交给gather_paths
        yield
    finally:
        os.chdir(this_dir)


if __name__ == '__main__':
    with chdir("/home/tim/Downloads/wordpress"):
        gather_paths()
    input('Press return to continue.')

    run()
    with open('myanswers.txt', 'w') as f:
        while not answers.empty():
            f.write(f'{answers.get()}\n')
    print('done')
