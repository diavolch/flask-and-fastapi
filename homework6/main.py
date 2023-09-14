from fastapi import FastAPI
import uvicorn
import logging
from homework.homework6.models import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Hello World"}


'''Запросы для users'''


@app.get("/users/")
async def return_users():
    logger.info('Отработал GET запрос')
    query = users.select()
    return await db.fetch_all(query)


@app.get("/users/{user_id}", response_model=Users)
async def return_user(user_id: int):
    query = users.select().where(users.c.user_id == user_id)
    return await db.fetch_one(query)


@app.post("/users/", response_model=Users)
async def create_user(user: Users):
    logger.info('Отработал POST запрос')
    query = users.insert().values(user_id=user.user_id, name=user.name, email=user.email, password=user.password)
    last_record_id = await db.execute(query)
    return {**user.model_dump(), "user_id": last_record_id}


@app.put("/users/{user_id}", response_model=Users)
async def update_user(user_id: int, new_user: Users):
    query = users.update().where(users.c.user_id == user_id).values(**new_user.model_dump())
    await db.execute(query)
    return {**new_user.model_dump(), "user_id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.user_id == user_id)
    await db.execute(query)
    return {'message': 'User deleted'}


'''Запросы для items'''


@app.get("/items/")
async def return_items():
    logger.info('Отработал GET запрос')
    query = items.select()
    return await db.fetch_all(query)


@app.get("/items/{item_id}", response_model=Items)
async def return_item(item_id: int):
    query = items.select().where(items.c.item_id == item_id)
    return await db.fetch_one(query)


@app.post("/items/", response_model=Items)
async def create_item(item: Items):
    logger.info('Отработал POST запрос')
    query = items.insert().values(item_id=item.user_id, title=item.title, description=item.description, price=item.price)
    last_record_id = await db.execute(query)
    return {**item.model_dump(), "item_id": last_record_id}


@app.put("/items/{item_id}", response_model=Items)
async def update_item(item_id: int, new_item: Items):
    query = items.update().where(items.c.item_id == item_id).values(**new_item.model_dump())
    await db.execute(query)
    return {**new_item.model_dump(), "item_id": item_id}


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    query = items.delete().where(items.c.item_id == item_id)
    await db.execute(query)
    return {'message': 'Item deleted'}


'''Запросы для orders'''


@app.get("/orders/")
async def return_orders():
    logger.info('Отработал GET запрос')
    query = orders.select()
    return await db.fetch_all(query)


@app.get("/orders/{order_id}", response_model=Orders)
async def return_order(order_id: int):
    query = orders.select().where(orders.c.order_id == order_id)
    return await db.fetch_one(query)


@app.post("/orders/", response_model=Orders)
async def create_order(order: Orders):
    logger.info('Отработал POST запрос')
    query = orders.insert().values(order_id=order.order_id, user_id=order.user_id, item_id=order.item_id)
    last_record_id = await db.execute(query)
    return {**order.model_dump(), "order_id": last_record_id}


@app.put("/orders/{order_id}", response_model=Orders)
async def update_order(order_id: int, new_order: Orders):
    query = orders.update().where(orders.c.order_id == order_id).values(**new_order.model_dump())
    await db.execute(query)
    return {**new_order.model_dump(), "order_id": order_id}


@app.delete("/orders/{order_id}/")
async def delete_item(order_id: int):
    query = orders.delete().where(orders.c.order_id == order_id)
    await db.execute(query)
    return {'message': 'Order deleted'}


if __name__ == "__main__":
    uvicorn.run("master:app", host='127.0.0.1', port=8000, reload=True)