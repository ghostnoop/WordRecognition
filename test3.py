import asyncio
import multiprocessing
import random
from multiprocessing.connection import Connection
from typing import List

from tortoise import Tortoise

from db import Config
from models.Comment import Comment
from modules.CustomConnection import CustomConnection


def child(connection: CustomConnection):
    while True:
        data: Comment = connection.receive(wait=True)
        s = f'{connection.index} ## {data.id}'
        print(s)

        connection.send(data)

    pass


async def async_worker(connections: dict, main_connection: Connection, processes: int):
    config = Config()
    await Tortoise.init(
        db_url=str(config.DATABASE_URL()),
        modules={'models': ['models.Comment']}
    )

    while True:
        comments = await Comment.filter().limit(2)
        size = len(comments)
        for comment in comments:
            idx = random.randint(0, processes-1)
            conn: Connection = connections[idx]
            conn.send(comment)

        for i in range(size):
            comment: Comment = main_connection.recv()
            print('main',comment.id)
            # await comment.save()


def worker(connections: dict, main_connection: Connection, processes: int):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(async_worker(connections, main_connection, processes))

    pass


if __name__ == '__main__':
    processes = 2
    main_receive, main_sendler = multiprocessing.Pipe(duplex=False)
    process_receiver_dct = {}

    tasks = []
    for index in range(processes):
        receive_connection, sendler_connection = multiprocessing.Pipe(duplex=False)
        cc = CustomConnection(index, receive_connection, main_sendler)
        process_receiver_dct[index] = sendler_connection
        task = multiprocessing.Process(target=child, args=(cc,), daemon=True)
        task.start()
        tasks.append(task)

    main_task = multiprocessing.Process(target=worker, args=(process_receiver_dct,
                                                             main_receive, processes),
                                        daemon=True)
    main_task.start()
    main_task.join()
