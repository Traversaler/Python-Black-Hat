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
