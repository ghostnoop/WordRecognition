import asyncio
import multiprocessing
import random
import sys
import time
from datetime import datetime
from multiprocessing.connection import Connection
from typing import List

from tortoise import Tortoise

from db import Config
from models.Comment import Comment
from modules.CustomConnection import CustomConnection
from worker import main_work


def child(connection: CustomConnection):
    while True:
        comment = connection.receive(wait=True)
        try:
            comment.id
        except Exception:
            print('comment is none', 'index', connection.index)
            time.sleep(10)
            continue
        comment.text = comment.text[:333]
        profanity, mood, emojis = main_work(comment.text)
        comment.is_contain_profanity = profanity
        comment.emotion_text_type_id = mood
        comment.emoji = emojis
        comment.is_done = True

        while True:
            try:
                connection.send(comment)
                break
            except Exception as e:
                print(e, 'connection error', connection.index)
                time.sleep(5)


def time_print(*args):
    print(*args, 'time:', datetime.now().strftime('%H:%M %d.%m'))


async def async_worker(connections: dict, main_connection: Connection, processes: int):
    config = Config()
    await Tortoise.init(
        db_url=str(config.DATABASE_URL()),
        modules={'models': ['models.Comment']}
    )
    print(str(config.DATABASE_URL()))

    while True:
        # comments = await Comment.filter(is_done=False).limit(500)
        comments = await Comment.filter(id__in=[28930317, 28930318, 28930319, 28930320, 28930321, 28930322, 28930323, 28930324, 28930325, 28930326, 28930327, 28930328, 28930329, 28930330, 28930331, 28930332, 28930333, 28930334, 28930335, 28930336, 28930337, 28930338, 28930339, 28930340, 28930341, 28930342, 28930343, 28930344, 28930345, 28930346, 28930347, 28930348, 28930349, 28930350, 28930351, 28930352, 28930353, 28930354, 28930355, 28930417, 28930356, 28930357, 28930358, 28930359, 28930360, 28930361, 28930362, 28930363, 28930364, 28930365])
        size = len(comments)
        time_print('len', size)
        if size == 0:
            time.sleep(10)
            continue

        for comment in comments:
            idx = random.randint(0, processes - 1)
            conn: Connection = connections[idx]
            conn.send(comment)
        counter = 0
        for i in range(size):
            comment: Comment = main_connection.recv()
            s = f'[ {counter} of {size} ] = '

            time_print(s, 'main', comment.id, comment.emotion_text_type_id,
                       comment.is_contain_profanity, comment.emoji,
                       comment.text.replace('\n', ''))
            await comment.save(update_fields=['emotion_text_type_id', 'is_contain_profanity', 'emoji', 'is_done'])
            counter += 1


def worker(connections: dict, main_connection: Connection, processes: int):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(async_worker(connections, main_connection, processes))


if __name__ == '__main__':
    processes = 20
    print(processes)
    time.sleep(1)

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
