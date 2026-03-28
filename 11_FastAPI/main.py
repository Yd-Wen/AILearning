from typing import Union

from fastapi import FastAPI, Path, Query, HTTPException, Depends
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int = Path(default=..., gt=0, le=1000, description="The ID of the item to get: 1-1000")):
    return {"item_id": item_id + 1}


@app.get("/news/news_list")
async def get_news_list(
        skip: int = Query(default=1, gt=0, le=1000, description="skip"),
        limit: int = Query(default=10, gt=0, le=1000, description="limit")
):
    return {"news_list": [{"id": i, "title": f"新闻标题{i}"} for i in range(skip, skip + limit)]}


@app.get("/news/{id}")
async def get_news_id(id: int):
    id_list = [i for i in range(1, 10)]
    if id not in id_list:
        raise HTTPException(status_code=404, detail="新闻不存在")
    return {"id": id, "title": f"新闻标题{id}"}


class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=10, description="用户名")
    password: str = Field(..., min_length=6, max_length=12, description="密码")


@app.post("/user/register")
async def register(user: User):
    return {"user": user, "message": "注册成功"}


@app.get("/html", response_class=HTMLResponse)
async def get_html():
    return """
    <html>
        <head>
            <title>HTML Response</title>
        </head>
        <body>
            <h1>Hello World</h1>
        </body>
    </html>
    """


@app.get("/file")
async def get_file():
    return FileResponse("./file/jjy.jpg")


class Books(BaseModel):
    id: int = Field(..., gt=0, description="id")
    name: str = Field(..., min_length=2, max_length=10, description="书名")
    author: str = Field(..., min_length=2, max_length=10, description="作者")
    price: float = Field(..., gt=0, description="价格")


@app.get("/books/{book_id}")
async def get_book(book_id: int):
    return {
        "id": book_id,
        "name": f"《Python 3.10 语言基础: {book_id}》",
        "author": "王",
        "price": 59.9
    }


@app.middleware("http")
async def middleware_1(request, call_next):
    print("中间件1 start...")
    response = await call_next(request)
    print("中间件1 end...")
    return response


@app.middleware("http")
async def middleware_2(request, call_next):
    print("中间件2 start...")
    response = await call_next(request)
    print("中间件2 end...")
    return response


async def common_parameters(
        skip: int = Query(default=0, ge=0), limit: int = Query(default=10, le=60)
):
    return {"skip": skip, "limit": limit}


@app.get("/user_list")
async def get_user_list(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/book_list")
async def get_book_list(commons: dict = Depends(common_parameters)):
    return commons

