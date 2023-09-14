from fastapi import FastAPI
import uvicorn
import logging
from homework.homework5.models import TaskBase, db, Task, Base, engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.get("/tasks/")
async def return_tasks():
    result = []
    logger.info('Отработал GET запрос')
    tasks = db.query(TaskBase).all()
    for task in tasks:
        result.append(f" title: {task.title}, description: {task.description}, status: {task.status} ")
    return result


@app.post("/tasks/")
async def create_task(new_task: Task):
    logger.info("Отработал POST запрос.")
    task_id = 1
    tasks = db.query(TaskBase).all()
    if db.query(TaskBase.task_id).first():
        for task in tasks:
            if task_id == task.task_id:
                task_id += 1
            else:
                break
        new_note = TaskBase(task_id=task_id, title=new_task.title, description=new_task.description, status=new_task.status)
        db.add(new_note)
        db.commit()
        return f'Task: {new_note}'


@app.get("/tasks/{task_id}")
async def get_id(task_id: int):
    logger.info("Отработал GET запрос.")
    task = db.query(TaskBase).filter(TaskBase.task_id == task_id).first()
    return f'Task: title: {task.title}, description: {task.description}, status: {task.status} '


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task_for_update: Task):
    logger.info("Отработал PUT запрос.")
    task = db.query(TaskBase).filter(TaskBase.task_id == task_id).first()
    task.title = task_for_update.title
    task.description = task_for_update.description
    task.status = task_for_update.status
    db.commit()
    return {"task_id": task_id, "task": task_for_update}


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    logger.info("Отработал DELETE запрос.")
    task = db.query(TaskBase).filter(TaskBase.task_id == task_id).first()
    db.delete(task)
    db.commit()
    return {"task_id": task_id}


if __name__ == "__main__":
    uvicorn.run("master:app", host='127.0.0.1', port=8000, reload=True)