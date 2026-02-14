# Sales-Analytics-Dashboard
<div align="center">
  <h1>Business Intelligence Dashboard</h1>
  <p><i>Интерактивная аналитика продаж на Python</i></p>
  
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg">
  <img src="https://img.shields.io/badge/Dash-2.14.0-green.svg">
  <img src="https://img.shields.io/badge/Plotly-5.17.0-orange.svg">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg">
  
  <br>
  <img src="screenshots/dashboard-preview.png" alt="Dashboard Preview" width="800">
</div>

## О проекте

Профессиональный дашборд для анализа продаж, созданный с использованием Python, Dash и Plotly. Проект демонстрирует навыки работы с данными, их визуализацию и создание интерактивных отчетов.

### Ключевые возможности

- Интерактивные фильтры по дате, категориям и регионам
- KPI метрики в реальном времени
- Визуализация трендов и сезонности
- Анализ по категориям** и регионам
- Тепловая карта сезонности продаж

## Технологический стек

| Технология | Назначение |
|------------|------------|
| Python 3.10 | Основной язык программирования |
| Dash | Фреймворк для создания дашборда |
| Plotly | Интерактивные графики |
| Pandas | Обработка и анализ данных |
| NumPy | Математические операции |
| Streamlit | Альтернативный вариант дашборда |


## Структура дашборда
business-dashboard
┣  data/ # Генерируемые данные
┣  src/ # Исходный код
┃ ┣  dashboard.py # Основной дашборд (Dash)
┃ ┣  generate_data.py # Генерация данных
┃ ┗  utils.py # Вспомогательные функции
┣ screenshots/ # Скриншоты для README
┣  requirements.txt # Зависимости
┣  insights.md # Аналитика и выводы
┗  README.md # Документация

## Быстрый старт

### Предварительные требования
- Python 3.8 или выше
- Git

### Установка и запуск

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/your-username/business-dashboard.git
cd business-dashboard

# 2. Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # для Mac/Linux
# venv\Scripts\activate    # для Windows

# 3. Установите зависимости
pip install -r requirements.txt

# 4. Сгенерируйте тестовые данные
python src/generate_data.py

# 5. Запустите дашборд
python src/dashboard.py

# 6. Откройте браузер
# Перейдите по адресу: http://localhost:8050
