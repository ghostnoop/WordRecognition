import multiprocessing
import random
import time
from multiprocessing import connection


def child(conn: connection.Connection, index: int):
    while True:
        conn.send(f'{random.random()}, index={index}')
        time.sleep(2)

    pass


def worker(conn: connection.Connection):
    st = time.monotonic()
    arr = []
    while True:
        if conn.poll():
            message = conn.recv()
            arr.append(message)

        if time.monotonic() - st > 5 or len(arr) > 10:
            print('in block')
            for i in arr:
                print(i)
            print('end block')
            arr.clear()
            st = time.monotonic()


if __name__ == '__main__':
    parent_conn, child_conn = multiprocessing.Pipe()
    processes = [index for index in range(3)]
    for process in processes:
        task = multiprocessing.Process(target=child, args=(child_conn, process), daemon=True)
        task.start()

    task = multiprocessing.Process(target=worker, args=(parent_conn,), daemon=True)
    task.start()
    task.join()
