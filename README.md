# Лабораторная работа №12

**ФИО:** Агапов Степан 

**Группа:** 221331

**Вариант:** 19 - Сервис заказа такси 

## Выполненные задания (повышенная сложность)

- **Задание 1** — Полноценное FastAPI приложение (JWT + CRUD + аналитика)
- **Задание 2** — Code review (`CODE_REVIEW.md`, анализ и исправление проблем)
- **Задание 4** — GitHub Actions CI/CD с AI-ревью Pull Request (`.github/workflows/ai-review.yml`)
- **Задание 7** — Unit-тесты с покрытием ≥90%

## Возможности проекта

- JWT авторизация
- Регистрация и логин пользователей
- CRUD операции
- Аналитика поездок
- Unit-тестирование
- AI code review через Gemini API
- Coverage отчёты
- GitHub Actions CI/CD

## Запуск проекта

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger UI:

```text
http://localhost:8000/docs
```

## Запуск тестов

```bash
coverage run -m pytest tests/ -v
coverage report -m
coverage html
```

## Структура тестов

- `tests/test_auth.py`
- `tests/test_rides.py`
- `tests/test_analytics.py`

## Используемые технологии

- FastAPI
- SQLAlchemy
- Pydantic
- JWT
- Pytest
- Coverage.py
- GitHub Actions
- Gemini API

## Результаты тестирования

- 23 unit-теста
- Coverage ≥90%
- Проверены edge cases
- Проверены негативные сценарии
- Проверены ошибки валидации
- Проверены CRUD операции
