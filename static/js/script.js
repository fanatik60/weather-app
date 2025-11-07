class WeatherApp {
    constructor() {
        this.interval = 30000; // 30 секунд
        this.init();
    }

    async init() {
        await this.updateWeather();
        this.startAutoUpdate();
        
        // Добавляем обработчик ошибок для фоновых изображений
        document.getElementById('background').addEventListener('error', (e) => {
            console.log('Ошибка загрузки фона, используем fallback');
            this.setFallbackBackground();
        });
    }

    async updateWeather() {
        try {
            const response = await fetch('/api/weather/random');
            const data = await response.json();

            if (data.error) {
                console.error('Ошибка:', data.error);
                this.showError();
                return;
            }

            this.updateDisplay(data);
        } catch (error) {
            console.error('Ошибка получения данных:', error);
            this.showError();
        }
    }

    updateDisplay(data) {
        // Обновляем фоновое изображение
        this.updateBackground(data.city_name);
        
        // Обновляем флаг
        this.updateFlag(data.country_code);
        
        // Обновляем название города и страны
        document.getElementById('city-name').textContent = data.city_name;
        document.getElementById('country-name').textContent = data.country;
        
        // Обновляем температуру с цветом
        this.updateTemperature(data.temperature, data.feels_like);
        
        // Обновляем иконку и описание погоды
        document.getElementById('weather-icon').textContent = data.icon;
        document.getElementById('conditions').textContent = data.conditions;
        
        // Обновляем влажность
        document.getElementById('humidity').textContent = Math.round(data.humidity);
        
        // Добавляем анимацию появления
        this.animateElements();
    }

    updateTemperature(temp, feelsLike) {
        const tempElement = document.getElementById('temperature');
        const feelsLikeElement = document.getElementById('feels-like');
        
        tempElement.textContent = `${temp > 0 ? '+' : ''}${temp}°C`;
        feelsLikeElement.textContent = `${feelsLike > 0 ? '+' : ''}${feelsLike}°C`;
        
        // Убираем все классы цвета
        tempElement.classList.remove('positive', 'negative');
        feelsLikeElement.parentElement.classList.remove('positive', 'negative');
        
        // Добавляем соответствующий класс цвета
        if (temp >= 0) {
            tempElement.classList.add('positive');
            feelsLikeElement.parentElement.classList.add('positive');
        } else {
            tempElement.classList.add('negative');
            feelsLikeElement.parentElement.classList.add('negative');
        }
    }

    updateBackground(cityName) {
        // Используем Unsplash для красивых городских изображений с современным стилем
        const queries = [
            `${cityName} city modern skyline night`,
            `${cityName} urban architecture contemporary`,
            `${cityName} downtown lights evening`,
            `${cityName} cityscape modern buildings`,
            `${cityName} metropolis night view`
        ];
        
        const randomQuery = queries[Math.floor(Math.random() * queries.length)];
        const backgroundUrl = `https://source.unsplash.com/1920x1080/?${encodeURIComponent(randomQuery)}`;
        
        // Предзагрузка изображения
        const img = new Image();
        img.onload = () => {
            document.getElementById('background').style.backgroundImage = `url('${backgroundUrl}')`;
        };
        img.onerror = () => {
            this.setFallbackBackground();
        };
        img.src = backgroundUrl;
    }

    setFallbackBackground() {
        // Современные градиенты для fallback
        const modernGradients = [
            'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
            'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
            'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
            'linear-gradient(135deg, #d299c2 0%, #fef9d7 100%)'
        ];
        const randomGradient = modernGradients[Math.floor(Math.random() * modernGradients.length)];
        document.getElementById('background').style.backgroundImage = randomGradient;
    }

    updateFlag(countryCode) {
        const flagElement = document.getElementById('flag');
        const flagUrl = `/static/flags/${countryCode}.png`;
        
        // Очищаем контейнер флага
        flagElement.innerHTML = '';
        
        // Создаем изображение флага
        const flagImg = new Image();
        flagImg.onload = () => {
            flagElement.appendChild(flagImg);
            // Добавляем анимацию появления флага
            flagImg.style.animation = 'slideIn 0.6s ease-out';
        };
        flagImg.onerror = () => {
            // Если флаг не найден, используем fallback
            flagImg.src = '/static/flags/fallback.png';
            flagElement.appendChild(flagImg);
        };
        flagImg.src = flagUrl;
        flagImg.alt = countryCode;
        flagImg.className = 'flag';
    }

    animateElements() {
        const elements = document.querySelectorAll('.weather-card > *');
        elements.forEach((element, index) => {
            element.style.animation = 'none';
            setTimeout(() => {
                element.style.animation = `slideIn 0.6s ease-out ${index * 0.1}s both`;
            }, 10);
        });
    }

    showError() {
        document.getElementById('city-name').textContent = 'Ошибка загрузки';
        document.getElementById('country-name').textContent = '---';
        document.getElementById('temperature').textContent = '--°C';
        document.getElementById('conditions').textContent = 'Нет данных';
        this.setFallbackBackground();
    }

    startAutoUpdate() {
        setInterval(() => {
            this.updateWeather();
        }, this.interval);
    }
}

// Запуск приложения когда страница загружена
document.addEventListener('DOMContentLoaded', () => {
    new WeatherApp();
});