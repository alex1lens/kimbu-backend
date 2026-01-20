from fastapi import FastAPI

app = FastAPI()

# Имитация базы данных (позже подключим настоящую)
numbers_db = {
    "79001112233": {"name": "Kimbu: Доставка пиццы", "type": "Бизнес"},
    "79110000000": {"name": "Kimbu: Мошенники!", "type": "Спам"}
}

@app.get("/")
def home():
    return {"status": "Kimbu Brain is Online"}

@app.get("/check/{phone}")
def check_number(phone: str):
    # Очищаем номер от лишних знаков (оставляем только цифры)
    clean_phone = "".join(filter(str.isdigit, phone))
    info = numbers_db.get(clean_phone)
    if info:
        return info
    return {"name": "Неизвестно", "type": "Нет данных"}