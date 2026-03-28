from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import DateTime, func, String, Float, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
app = FastAPI()

# 1. 创建异步引擎
ASYNC_DATABASE_URL = "mysql+aiomysql://root:041209@localhost:3306/fastapi_test?charset=utf8mb4"
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,           # 输出 SQL 日志
    pool_size=20,        # 连接池大小
    max_overflow=10,     # 连接池溢出大小
)


# 2. 定义模型类 基类 + 表对应的模型类
class Base(DeclarativeBase):
    """
    定义模型类基类
    """
    create_time: Mapped[datetime] = (
        mapped_column(DateTime, insert_default=func.now(), default=datetime.now, comment="创建时间"))
    update_time: Mapped[datetime] = (
        mapped_column(DateTime, insert_default=func.now(), default=datetime.now, onupdate=func.now(), comment="更新时间"))


class Book(Base):
    """
    定义模型类
    """
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="编号")
    title: Mapped[str] = mapped_column(String(50), nullable=False, comment="标题")
    author: Mapped[str] = mapped_column(String(50), nullable=False, comment="作者")
    price: Mapped[float] = mapped_column(Float, nullable=False, comment="价格")


# 3. 建表
# 3.1 开启事务，执行ORM操作
async def create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # 基类元数据创建表


# 3.2 应用启动时建表
@app.on_event("startup")
async def startup():
    await create_table()


async_session = async_sessionmaker(
    bind=async_engine,       # 绑定引擎
    class_=AsyncSession,     # 指定会话类 使用异步会话
    expire_on_commit=False   # 提交后会话不过期
)


# 依赖项
async def get_database():
    """
    获取数据库连接
    :return:
    """
    async with async_session() as session:
        try:
            yield session                # 返回数据库会话
            await session.commit()       # 提交事务
        except Exception as e:
            await session.rollback()     # 回滚
            raise e


@app.get("/book/books")
async def get_books(db: AsyncSession = Depends(get_database)):
    """
    获取所有图书
    :param db:
    :return:
    """
    query = await db.execute(select(Book))
    # books = query.scalars().all()
    # book = query.scalars().first()
    return await db.get(Book, 1)
    # return books


@app.get("/book/id/{book_id}")
async def get_book(book_id: int, db: AsyncSession = Depends(get_database)):
    """
    获取所有图书
    :param book_id:
    :param db:
    :return:
    """
    query = await db.execute(select(Book).where(Book.id == book_id))
    return query.scalar_one_or_none()


@app.get("/book/count")
async def get_book_count(db: AsyncSession = Depends(get_database)):
    """
    获取图书数量
    :param db:
    :return:
    """
    query = await db.execute(select(func.count(Book.id)))
    return query.scalar()


@app.get("/books/page")
async def get_books_page(page: int = 1, page_size: int = 10, db: AsyncSession = Depends(get_database)):
    """
    获取图书分页
    :param page:
    :param page_size:
    :param db:
    :return:
    """
    query = await db.execute(select(Book).offset((page - 1) * page_size).limit(page_size))
    return query.scalars().all()


class BookBase(BaseModel):
    title: str
    author: str
    price: float


@app.post("/book/add")
async def add_book(book: BookBase, db: AsyncSession = Depends(get_database)):
    """
    添加图书
    :param book:
    :param db:
    :return:
    """
    # 获取 book 参数，创建 Book 实例
    book_obj = Book(**book.__dict__)
    db.add(book_obj)
    await db.commit()
    return book


@app.put("/book/update/{book_id}")
async def update_book(book_id: int, data: BookBase, db: AsyncSession = Depends(get_database)):
    """
    更新图书
    :param book_id:
    :param data:
    :param db:
    :return:
    """
    # 1. 查询
    book = await db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    # 2. 更新
    book.title = data.title
    book.author = data.author
    book.price = data.price
    # 3. 提交
    await db.commit()
    return book


@app.delete("/book/delete/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_database)):
    """
    删除图书
    :param book_id:
    :param db:
    :return:
    """
    # 1. 获取图书
    book = await db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    # 2. 删除
    await db.delete(book)
    # 3. 提交
    await db.commit()
    return {"message": "Book deleted"}

