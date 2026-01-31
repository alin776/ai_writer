import asyncio
from app.core.database import SessionLocal
from sqlalchemy import select
from app.models.user_task import TaskTemplate

async def check():
    async with SessionLocal() as db:
        result = await db.execute(
            select(TaskTemplate).where(TaskTemplate.task_key == 'daily_channel_messages')
        )
        task = result.scalar_one_or_none()
        print(f'Task found: {task}')
        if task:
            print(f'Title: {task.title}')
            print(f'Description: {task.description}')
            print(f'Reward: {task.reward_credits}')
            print(f'Type: {task.task_type}')
            print(f'Config: {task.target_config}')
        else:
            print('Task not found!')

if __name__ == "__main__":
    asyncio.run(check())
