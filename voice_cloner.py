///// РАБОТАЕТ НА ПИТОНЕ ВЕРСИИ 3.9-3.11
///// виртуалку делал такую voice_env\Scripts\activate    pip install coqui-tts
///// pip install torch torchaudio
///// дальше писать не буду, т.к. ошибки были у меня


import torch
from TTS.api import TTS
import os
import time
import sys

# 1. Укажите путь к файлу, который вы записали с помощью вашей первой программы.
# Убедитесь, что файл 'recorded_audio.wav' находится в той же папке, что и этот скрипт.
SAMPLE_WAV = "recorded_audio.wav"

# 2. Текст, который вы хотите озвучить клонированным голосом.
# Попробуйте написать что-то на том языке, на котором говорил человек в записи.
TEXT_TO_SPEAK = "Привет! Это мой клонированный голос, и он говорит то, что я хочу."

# 3. Инициализируем модель XTTSv2.
# Параметр gpu=False означает, что мы будем использовать процессор. Если у вас есть видеокарта NVIDIA, поставьте True — будет быстрее.
print("Загрузка модели XTTSv2... Это может занять некоторое время при первом запуске.")
try:
    # Важно: при первом вызове модель автоматически скачается из интернета (~2 ГБ).
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
    print("Модель загружена.")
except Exception as e:
    print(f"Ошибка при загрузке модели: {e}")
    print("Проверьте подключение к интернету и установку TTS (pip install TTS).")
    sys.exit()

# 4. Проверяем, существует ли файл с образцом голоса.
if not os.path.exists(SAMPLE_WAV):
    print(f"ОШИБКА: Файл {SAMPLE_WAV} не найден!")
    print("Убедитесь, что вы сначала записали голос с помощью первой программы.")
    sys.exit()

# 5. Запускаем процесс клонирования и синтеза.
print(f"\nНачинаю обработку...")
print(f"Образец голоса: {SAMPLE_WAV}")
print(f"Текст для озвучки: '{TEXT_TO_SPEAK}'")

# Замеряем время выполнения
start_time = time.time()

# Функция tts.tts_to_file делает всю магию:
# - speaker_wav: путь к файлу-образцу голоса.
# - text: текст для произнесения.
# - language: язык текста. XTTSv2 поддерживает русский ('ru'), английский ('en') и многие другие.
# - file_path: куда сохранить итоговый аудиофайл.
tts.tts_to_file(
    text=TEXT_TO_SPEAK,
    speaker_wav=SAMPLE_WAV,
    language="ru",
    file_path="cloned_output.wav"
)

end_time = time.time()
print(f"\nГОТОВО!")
print(f"Аудиофайл сохранен как 'cloned_output.wav' в текущей папке.")
print(f"Время обработки: {end_time - start_time:.2f} секунд.")
