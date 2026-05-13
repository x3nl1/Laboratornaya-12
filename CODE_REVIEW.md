
# Code Review — задание 2

## Что сгенерировал ИИ → В чём проблема → Как исправил

### 1. Захардкоженный SECRET_KEY

**Что сгенерировал ИИ:**
```python
SECRET_KEY = "qwerty"
```

**Проблема:**  
Это уязвимость безопасности.
Секрет может попасть в репозиторий.

**Исправил:**  
Перенёс в переменные окружения через os.getenv().

```python
SECRET_KEY = os.getenv("SECRET_KEY", "qwerty")
```

---

### 2. Отсутствие rollback при ошибке регистрации

**Что сгенерировал ИИ:**
```python
db.add(db_user)
db.commit()
```

**Проблема:**  
Если commit завершится ошибкой, сессия БД остаётся в неконсистентном состоянии.

**Исправил:**  
Добавил обработку ошибок и rollback:

```python
try:
    db.add(db_user)
    db.commit()
except Exception:
    db.rollback()
    raise
```

---

### 3. Отсутствие проверки цены поездки

**Что сгенерировал ИИ:**
```python
class RideCreate(BaseModel):
    price: float
```

**Проблема:**  
API принимал отрицательные значения стоимости поездки.

**Исправил:**  
Добавил валидацию через Pydantic:

```python
class RideCreate(BaseModel):
    price: float = Field(gt=0)
```

---

### 4. Создание поездки без проверки существования связанных сущностей

**Что сгенерировал ИИ:**
```python
db_ride = Ride(**ride.dict())
db.add(db_ride)
db.commit()
```

**Проблема:**  
Можно было создать поездку с несуществующим пользователем, водителем или тарифом.

**Исправил:**  
Добавил проверки перед созданием:

```python
if not db.query(User).filter(User.id == ride.user_id).first():
    raise HTTPException(404, "User not found")

if not db.query(Driver).filter(Driver.id == ride.driver_id).first():
    raise HTTPException(404, "Driver not found")
```

---

### 5. Некорректная аналитика на пустой БД

**Что сгенерировал ИИ:**
```python
return {
    "total_rides": len(rides),
    "total_revenue": sum(r.price for r in rides)
}
```

**Проблема:**  
На пустой базе edge-case не был обработан явно.

**Исправил:**  
Добавил безопасную обработку:

```python
total_revenue = sum(ride.price for ride in rides) if rides else 0

return {
    "total_rides": len(rides),
    "total_revenue": total_revenue
}
```

---

### 6. Отсутствие индекса на часто используемом поле

**Что сгенерировал ИИ:**
```python
plate_number = Column(String, unique=True)
```

**Проблема:**  
Поиск по номеру автомобиля выполнялся без индекса — полный scan таблицы.

**Исправил:**  
Добавил индекс:

```python
plate_number = Column(String, unique=True, index=True)
```

---

## Итог

Найдено и исправлено: **6 проблем**

Категории исправлений:

- безопасность
- обработка исключений
- логические ошибки
- валидация данных
- производительность
- устойчивость edge-case сценариев