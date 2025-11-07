import os
import requests
import json
from urllib.parse import urljoin

def download_flags():
    """Скачивает флаги для всех городов из списка"""
    
    # Создаем папку для флагов
    flags_dir = 'static/flags'
    os.makedirs(flags_dir, exist_ok=True)
    
    # Загружаем список городов
    with open('cities.json', 'r', encoding='utf-8') as f:
        cities = json.load(f)
    
    # Получаем уникальные коды стран
    country_codes = set(city['country_code'].lower() for city in cities)
    
    print(f"Найдено {len(country_codes)} уникальных стран")
    print("Начинаем загрузку флагов...")
    
    downloaded = 0
    errors = 0
    
    for country_code in country_codes:
        flag_filename = f"{flags_dir}/{country_code}.png"
        
        # Если файл уже существует, пропускаем
        if os.path.exists(flag_filename):
            downloaded += 1
            continue
            
        try:
            # Пробуем разные источники для флагов
            sources = [
                f"https://flagcdn.com/w320/{country_code}.png",
                f"https://flagsapi.com/{country_code.upper()}/flat/64.png",
                f"https://www.worldometers.info/img/flags/{country_code}-flag.gif",
            ]
            
            for url in sources:
                try:
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        with open(flag_filename, 'wb') as f:
                            f.write(response.content)
                        print(f"✓ Скачан флаг: {country_code}")
                        downloaded += 1
                        break
                except:
                    continue
            else:
                print(f"✗ Ошибка загрузки флага: {country_code}")
                errors += 1
                
        except Exception as e:
            print(f"✗ Ошибка с {country_code}: {e}")
            errors += 1
    
    print(f"\nЗагрузка завершена!")
    print(f"Успешно: {downloaded}")
    print(f"Ошибок: {errors}")
    
    # Создаем fallback флаг
    create_fallback_flag(flags_dir)

def create_fallback_flag(flags_dir):
    """Создает fallback флаг для случаев когда флаг не найден"""
    from PIL import Image, ImageDraw
    
    # Создаем простой флаг с символом вопроса
    img = Image.new('RGB', (320, 240), color='gray')
    draw = ImageDraw.Draw(img)
    
    # Добавляем белый прямоугольник
    draw.rectangle([10, 10, 310, 230], outline='white', width=2)
    
    # Добавляем вопросительный знак
    from PIL import ImageFont
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()
    
    draw.text((160, 120), "?", fill='white', font=font, anchor="mm")
    
    img.save(f"{flags_dir}/fallback.png")
    print("✓ Создан fallback флаг")

if __name__ == '__main__':
    download_flags()