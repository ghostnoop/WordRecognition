import multiprocessing
import random
import sys
import time
from multiprocessing import connection


def child(conn: connection.Connection, index: int):
    counter = 0
    while True:
        t = conn.recv()
        counter += 1
        # time.sleep(index)
        # print(t, 'index', index, '\n', end=' ')
        s = f'\ncounter {counter}, index {index}\n'
        print(s)
        conn.send(index)

    # while True:
    #     conn.send(f'{random.random()}, index={index}')
    #     time.sleep(2)


def worker(conn: connection.Connection):
    for i in range(100):
        conn.send(i)

    time.sleep(3)
    dct = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    while True:
        if conn.poll():
            message = conn.recv()
            print('mess', message)
            dct[message] += 1
        else:
            break
    print(dct)

    # st = time.monotonic()
    # arr = []
    # while True:
    #     if conn.poll():
    #         message = conn.recv()
    #         arr.append(message)
    #
    #     if time.monotonic() - st > 5 or len(arr) > 10:
    #         print('in block')
    #         for i in arr:
    #             print(i)
    #         print('end block')
    #         arr.clear()
    #         st = time.monotonic()


if __name__ == '__main__':
    parent_conn, child_conn = multiprocessing.Pipe()
    processes = [index for index in range(3)]
    arr = []
    for process in processes:
        task = multiprocessing.Process(target=child, args=(child_conn, process), daemon=True)
        task.start()
        arr.append(task)

    main_task = multiprocessing.Process(target=worker, args=(parent_conn,), daemon=True)
    main_task.start()

    for task in arr:
        task.join()
