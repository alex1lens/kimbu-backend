from fastapi import FastAPI

app = FastAPI()

numbers_db = {
    "79001112233": {"name": "Kimbu: Доставка пиццы", "type": "Бизнес"}
}

@app.get("/")  # Главная страница
def home():
    return {"message": "Welcome to Kimbu API"}

@app.get("/check/{phone}")  # Тот самый путь
def check_number(phone: str):
    return numbers_db.get(phone, {"name": "Неизвестно"})
