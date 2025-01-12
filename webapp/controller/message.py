import asyncio
from fastapi import APIRouter

message_router = APIRouter(prefix="/message", tags=["聊天消息"])


async def call_chat_bot(message: str, queue: asyncio.Queue, robot_name="ChatBot"):
    print(f"{robot_name} 开始处理消息：{message}")
    asyncio.sleep(3)  # 模拟机器人处理消息

    reply_message = f"{robot_name} 回复消息：{message}"
    await queue.put(reply_message)
    await queue.join()
    ...

async def save_message(message: str):
    print(f"保存消息：{message}")
    asyncio.sleep(1)  # 模拟保存消息
    ...

async def handle_queue(queue: asyncio.Queue):

    while True:
        message = await queue.get()
        await save_message(message)
        queue.task_done()

        ...


async def call_message(message: str):
    

    # 启动任务
    running_tasks = set()
    queue = asyncio.Queue()
    async with asyncio.TaskGroup() as task_group:
        robot_list = ["Robot1", "Robot2", "Robot3"]
        for robot_name in robot_list:
            task = task_group.create_task(call_chat_bot(message, queue, robot_name))
            running_tasks.add(task)
            task.add_done_callback(running_tasks.discard)

    # 等待任务完成
    await task

    # 处理队列中的消息
    while not queue.empty():

    ...



@message_router.post("/call", summary="调用聊天机器人")
async def call_message(message: str):
    # 调用聊天机器人，返回回复消息
    reply_message = "这是聊天机器人的回复消息"


    

    return {"reply": reply_message}
