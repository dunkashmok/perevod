import pyaudio
import wave
import keyboard
import threading
import time
import numpy as np

class AudioProcessor:
    def __init__(self, sample_rate=16000, channels=1, chunk_size=1024, format_type=pyaudio.paInt16):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.format = format_type
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False
        self.stream = None
        
    def start_recording(self):
        """Начинает запись с микрофона в отдельном потоке."""
        self.is_recording = True
        self.frames = []
        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        print("Запись началась...")
        self.recording_thread = threading.Thread(target=self._record)
        self.recording_thread.start()
        
    def _record(self):
        """Внутренний метод для непрерывной записи аудио."""
        while self.is_recording:
            data = self.stream.read(self.chunk_size)
            self.frames.append(data)
            
    def stop_and_save_recording(self, filename="output.wav"):
        """Останавливает запись и сохраняет аудио в WAV-файл."""
        if self.stream:
            self.is_recording = False
            self.recording_thread.join()
            self.stream.stop_stream()
            self.stream.close()
            
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print(f"Аудио сохранено в {filename}")
        return filename
    
    def close(self):
        """Освобождает ресурсы PyAudio."""
        self.audio.terminate()

# Функция для простого управления записью через клавиатуру
def keyboard_recording():
    processor = AudioProcessor()
    print("Нажмите и удерживайте 'r' для записи, отпустите для сохранения.")
    recording_in_progress = False
    while True:
        if keyboard.is_pressed('r') and not recording_in_progress:
            processor.start_recording()
            recording_in_progress = True
            time.sleep(0.1)
        elif not keyboard.is_pressed('r') and recording_in_progress:
            processor.stop_and_save_recording("recorded_audio.wav")
            recording_in_progress = False
            print("Готово. Нажмите 'r' для новой записи или 'q' для выхода.")
        elif keyboard.is_pressed('q'):
            if recording_in_progress:
                processor.stop_and_save_recording("recorded_audio.wav")
            break
        time.sleep(0.05)
    processor.close()

if __name__ == "__main__":
    keyboard_recording()
