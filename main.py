import os
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Подключение к базе через переменную, которую мы настроили в Render
DATABASE_URL = os.getenv("DATABASE_URL")

# Настройка соединения
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Описание таблицы номеров
class PhoneRecord(Base):
    __tablename__ = "numbers"
    phone = Column(String, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)

# Создание таблицы при запуске
Base.metadata.create_all(bind=engine)

app = FastAPI()

class NumberInput(BaseModel):
    phone: str
    name: str
    category: str

@app.get("/check/{phone}")
def check(phone: str):
    db = SessionLocal()
    # Чистим номер от лишних знаков, если они придут
    clean_phone = "".join(filter(str.isdigit, phone))
    result = db.query(PhoneRecord).filter(PhoneRecord.phone == clean_phone).first()
    db.close()
    if result:
        return {"name": result.name, "category": result.category}
    return {"name": "Неизвестно", "category": "Нет данных"}

@app.post("/add_number")
def add(data: NumberInput):
    db = SessionLocal()
    new_record = PhoneRecord(phone=data.phone, name=data.name, category=data.category)
    db.merge(new_record) # Добавит или обновит, если номер уже есть
    db.commit()
    db.close()
    return {"status": "Сохранено в Postgres!"}

@app.get("/search/{phone}")
async def search_number(phone: str):
    # Тут логика поиска в твоей базе данных
    # Например:
    contacts = {"79991234567": "Иван (Доставка)", "79001112233": "Спам: Опросы"}
    name = contacts.get(phone, "Номер не найден")
    return {"name": name} 
