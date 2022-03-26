import asyncio
import multiprocessing
import random
import time
from multiprocessing.connection import Connection
from typing import List

from tortoise import Tortoise

from db import Config
from models.Comment import Comment
from modules.CustomConnection import CustomConnection
from worker import main_work


def child(connection: CustomConnection):
    while True:
        comment: Comment = connection.receive(wait=True)
        try:
            profanity, mood, emojis = main_work(comment.text)
            comment.is_contain_profanity = profanity
            comment.emotion_text_type_id = mood
            comment.emoji = emojis
            comment.is_done = True
        except Exception as e:
            print(e)
            pass
        connection.send(comment)


async def async_worker(connections: dict, main_connection: Connection, processes: int):
    config = Config()
    await Tortoise.init(
        db_url=str(config.DATABASE_URL()),
        modules={'models': ['models.Comment']}
    )

    while True:
        comments = await Comment.filter(is_done=False).limit(1_000)
        size = len(comments)
        for comment in comments:
            idx = random.randint(0, processes - 1)
            conn: Connection = connections[idx]
            conn.send(comment)
        counter = 0
        for i in range(size):
            comment: Comment = main_connection.recv()
            s = f'[ {counter} of {size} ] = '

            # print(s, 'main', comment.id, comment.emotion_text_type_id,
            #       comment.is_contain_profanity, comment.emoji,
            #       comment.text.replace('\n', ''))
            # await comment.save()
            counter += 1


def worker(connections: dict, main_connection: Connection, processes: int):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(async_worker(connections, main_connection, processes))


if __name__ == '__main__':
    processes = 50
    print(processes)
    time.sleep(2)

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
                                                             main_receive, processes), daemon=True)
    main_task.start()
    main_task.join()
