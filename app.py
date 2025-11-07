from flask import Flask, render_template, jsonify
import requests
import json
import os
from dotenv import load_dotenv
import random
from datetime import datetime

# Загрузка переменных окружения
load_dotenv()

app = Flask(__name__)

# Загрузка списка городов
with open('cities.json', 'r', encoding='utf-8') as f:
    CITIES = json.load(f)

# Словарь для перевода погодных условий
WEATHER_TRANSLATIONS = {
    'Clear': 'Ясно',
    'Sunny': 'Солнечно',
    'Partly cloudy': 'Переменная облачность',
    'Cloudy': 'Облачно',
    'Overcast': 'Пасмурно',
    'Rain': 'Дождь',
    'Rain, Partially cloudy': 'Дождь, Переменная облачность',
    'Rain, Overcast': 'Дождь, Пасмурно',
    'Snow': 'Снег',
    'Thunderstorm': 'Гроза',
    'Fog': 'Туман',
    'Mist': 'Дымка',
    'Partly Cloudy': 'Переменная облачность',
    'Mostly Cloudy': 'В основном облачно',
    'Light rain': 'Небольшой дождь',
    'Heavy rain': 'Сильный дождь',
    'Light snow': 'Небольшой снег',
    'Heavy snow': 'Сильный снег',
    'Drizzle': 'Морось',
    'Hail': 'Град',
    'Sleet': 'Мокрый снег',
    'Windy': 'Ветрено',
    'Breezy': 'Порывистый ветер',
    'Clear throughout the day.': 'Ясно в течение дня',
    'Possible light rain until evening.': 'Возможен небольшой дождь до вечера',
    'Light rain throughout the day.': 'Небольшой дождь в течение дня',
    'Overcast throughout the day.': 'Пасмурно в течение дня',
    'Foggy in the morning.': 'Туманно утром',
    'Partly cloudy throughout the day.': 'Переменная облачность в течение дня',
    'Mostly cloudy throughout the day.': 'В основном облачно в течение дня',
    'Rain throughout the day.': 'Дождь в течение дня',
    'Snow throughout the day.': 'Снег в течение дня'
}

# Словарь для иконок погоды на английском языке
WEATHER_ICONS = {
    'Clear': '☀️',
    'Sunny': '☀️',
    'Partly cloudy': '⛅',
    'Cloudy': '☁️',
    'Overcast': '☁️',
    'Mostly Cloudy': '☁️',
    'Partly Cloudy': '⛅',
    'Mist': '🌫️',
    'Fog': '🌫️',
    'Light fog': '🌫️',
    'Rain': '🌧️',
    'Light rain': '🌦️',
    'Heavy rain': '⛈️',
    'Moderate rain': '🌧️',
    'Drizzle': '🌦️',
    'Snow': '❄️',
    'Light snow': '🌨️',
    'Heavy snow': '❄️❄️',
    'Thunderstorm': '⛈️',
    'Storm': '⛈️',
    'Hail': '🧊',
    'Sleet': '🌨️💧',
    'Windy': '💨',
    'Breezy': '💨',
    'Clear throughout the day.': '☀️',
    'Possible light rain until evening.': '🌦️',
    'Light rain throughout the day.': '🌦️',
    'Overcast throughout the day.': '☁️',
    'Foggy in the morning.': '🌫️',
    'Partly cloudy throughout the day.': '⛅',
    'Mostly cloudy throughout the day.': '☁️',
    'Rain throughout the day.': '🌧️',
    'Snow throughout the day.': '❄️'
}

# Словарь для иконок погоды на русском языке
WEATHER_ICONS_RU = {
    # Ясная погода
    'Ясно': '☀️',
    'Солнечно': '☀️',
    'Ясно в течение дня': '☀️',
    
    # Облачность
    'Переменная облачность': '⛅',
    'Облачно': '☁️',
    'Пасмурно': '☁️',
    'В основном облачно': '☁️',
    'Переменная облачность в течение дня': '⛅',
    'В основном облачно в течение дня': '☁️',
    'Пасмурно в течение дня': '☁️',
    'Частично облачно': '⛅',
    
    # Туман и дымка
    'Туман': '🌫️',
    'Дымка': '🌫️',
    'Туманно утром': '🌫️',
    
    # Дождь
    'Дождь': '🌧️',
    'Небольшой дождь': '🌦️',
    'Сильный дождь': '⛈️',
    'Дождь, Переменная облачность': '🌦️',
    'Дождь, Пасмурно': '🌧️',
    'Морось': '🌦️',
    'Возможен небольшой дождь до вечера': '🌦️',
    'Небольшой дождь в течение дня': '🌦️',
    'Дождь в течение дня': '🌧️',
    
    # Снег
    'Снег': '❄️',
    'Небольшой снег': '🌨️',
    'Сильный снег': '❄️❄️',
    'Снег в течение дня': '❄️',
    
    # Гроза
    'Гроза': '⛈️',
    
    # Прочие
    'Град': '🧊',
    'Мокрый снег': '🌨️💧',
    'Ветрено': '💨',
    'Порывистый ветер': '💨'
}

def get_weather_icon(weather_description):
    """Умное определение иконки погоды (поддерживает русский и английский)"""
    if not weather_description or weather_description == 'Unknown':
        return '⛅'  # Используем облако вместо термометра
    
    print(f"🔍 Определение иконки для: '{weather_description}'")
    
    # Сначала проверяем русский словарь
    if weather_description in WEATHER_ICONS_RU:
        icon = WEATHER_ICONS_RU[weather_description]
        print(f"✅ Найдено в русском словаре: {icon}")
        return icon
    
    # Затем проверяем английский словарь
    if weather_description in WEATHER_ICONS:
        icon = WEATHER_ICONS[weather_description]
        print(f"✅ Найдено в английском словаре: {icon}")
        return icon
    
    # Поиск по ключевым словам на русском
    description_lower = weather_description.lower()
    
    if any(word in description_lower for word in ['ясн', 'солн']):
        icon = '☀️'
    elif any(word in description_lower for word in ['переменн', 'частичн']):
        icon = '⛅'
    elif any(word in description_lower for word in ['облачн', 'пасмурн']):
        icon = '☁️'
    elif any(word in description_lower for word in ['туман', 'дымк']):
        icon = '🌫️'
    elif any(word in description_lower for word in ['дожд', 'морос']):
        if any(word in description_lower for word in ['небольш', 'легк']):
            icon = '🌦️'
        elif any(word in description_lower for word in ['сильн', 'ливень']):
            icon = '⛈️'
        else:
            icon = '🌧️'
    elif any(word in description_lower for word in ['снег']):
        if any(word in description_lower for word in ['небольш', 'легк']):
            icon = '🌨️'
        else:
            icon = '❄️'
    elif any(word in description_lower for word in ['гроз', 'гром']):
        icon = '⛈️'
    elif any(word in description_lower for word in ['град', 'лед']):
        icon = '🧊'
    elif any(word in description_lower for word in ['ветр']):
        icon = '💨'
    else:
        # Если ничего не подошло, используем облако
        icon = '⛅'
        print(f"❓ Не удалось определить иконку, используется облако: {icon}")
    
    print(f"🎯 Определено по ключевым словам: {icon}")
    return icon

def get_city_background(city_name, country):
    """Создание уникального фона для каждого города"""
    try:
        # Создаем уникальный ID для города
        city_id = f"{city_name}_{country}".lower().replace(' ', '_')
        city_hash = hash(city_id)
        
        # Цветовая палитра на основе хеша
        hue1 = (city_hash % 360)
        hue2 = (city_hash + 120) % 360
        hue3 = (city_hash + 240) % 360
        
        # Варианты фонов
        background_options = [
            # Градиент 1
            f'linear-gradient(135deg, hsl({hue1}, 70%, 50%) 0%, hsl({hue2}, 70%, 60%) 100%)',
            
            # Градиент 2  
            f'linear-gradient(135deg, hsl({hue2}, 70%, 40%) 0%, hsl({hue3}, 70%, 50%) 100%)',
            
            # Градиент 3
            f'linear-gradient(135deg, hsl({hue3}, 70%, 30%) 0%, hsl({hue1}, 70%, 40%) 100%)',
            
            # Радиальный градиент
            f'radial-gradient(circle at 30% 20%, hsl({hue1}, 80%, 60%), hsl({hue2}, 80%, 40%))',
            
            # Конический градиент
            f'conic-gradient(from 90deg, hsl({hue1}, 70%, 50%), hsl({hue2}, 70%, 50%), hsl({hue3}, 70%, 50%))'
        ]
        
        # Выбираем вариант на основе хеша
        option_index = abs(city_hash) % len(background_options)
        return background_options[option_index]
        
    except Exception as e:
        print(f"Ошибка создания фона для {city_name}: {e}")
        return 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'

def get_weather_data(city):
    """Получение данных о погоде для города"""
    api_key = os.getenv('VISUAL_CROSSING_API_KEY')
    if not api_key:
        print("❌ API ключ не найден")
        return None
    
    try:
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city['lat']},{city['lon']}?unitGroup=metric&key={api_key}&contentType=json&lang=ru"
        
        print(f"🌐 Запрос погоды для {city['name']}...")
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Ошибка API: {response.status_code}")
            return None
            
        data = response.json()
        
        if 'currentConditions' not in data:
            print("❌ Нет данных о текущих условиях")
            return None
            
        current_conditions = data['currentConditions']
        
        # Получаем описание погоды
        weather_description = current_conditions.get('conditions', 'Unknown')
        print(f"📊 Получены условия: {weather_description}")
        
        # Переводим описание (если нужно)
        translated_description = WEATHER_TRANSLATIONS.get(weather_description, weather_description)
        
        # Определяем иконку
        weather_icon = get_weather_icon(weather_description)
        
        # Создаем уникальный фон для города
        print(f"🎨 Создание фона для {city['name']}...")
        city_background = get_city_background(city['name'], city['country'])
        
        return {
            'temperature': round(current_conditions['temp']),
            'feels_like': round(current_conditions['feelslike']),
            'humidity': current_conditions['humidity'],
            'conditions': translated_description,
            'icon': weather_icon,
            'city_name': city['name'],
            'country': city['country'],
            'country_code': city['country_code'].lower(),
            'city_photo': city_background
        }
    except Exception as e:
        print(f"❌ Ошибка получения погоды для {city['name']}: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather/random')
def get_random_weather():
    """Получение погоды для случайного города"""
    if not hasattr(get_random_weather, 'used_cities'):
        get_random_weather.used_cities = []
    
    # Если все города использованы, начинаем заново
    if len(get_random_weather.used_cities) >= len(CITIES):
        get_random_weather.used_cities = []
    
    # Выбираем случайный город из еще не использованных
    available_cities = [city for city in CITIES if city['name'] not in [uc['name'] for uc in get_random_weather.used_cities]]
    
    if not available_cities:
        get_random_weather.used_cities = []
        available_cities = CITIES.copy()
    
    city = random.choice(available_cities)
    get_random_weather.used_cities.append(city)
    
    weather_data = get_weather_data(city)
    
    if weather_data:
        return jsonify(weather_data)
    else:
        return jsonify({'error': 'Не удалось получить данные о погоде'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)