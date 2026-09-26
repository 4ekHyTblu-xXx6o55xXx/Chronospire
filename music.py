"""Процедурная генерация и воспроизведение музыки"""
import os
import wave
import numpy as np

try:
    import pygame
    PYGAME_OK = True
except ImportError:
    PYGAME_OK = False

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
SAMPLE_RATE = 22050


def _ensure_assets():
    os.makedirs(ASSETS_DIR, exist_ok=True)


def _sine(freq, duration, volume=0.3):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave_data = np.sin(freq * t * 2 * np.pi)
    # Envelope (fade in/out)
    fade = int(SAMPLE_RATE * 0.1)
    wave_data[:fade] *= np.linspace(0, 1, fade)
    wave_data[-fade:] *= np.linspace(1, 0, fade)
    return wave_data * volume


def _write_wav(path, signal):
    signal = np.clip(signal, -1.0, 1.0)
    data = (signal * 32767).astype(np.int16)
    with wave.open(path, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(data.tobytes())


def generate_calm(path):
    """Спокойная ambient-мелодия"""
    chords = [
        [220.00, 261.63, 329.63],
        [174.61, 220.00, 261.63],
        [261.63, 329.63, 392.00],
        [196.00, 246.94, 293.66],
    ]
    duration_per = 4.0
    total = duration_per * len(chords) * 2
    full = np.zeros(int(SAMPLE_RATE * total))
    pos = 0
    for _ in range(2):
        for chord in chords:
            seg = np.zeros(int(SAMPLE_RATE * duration_per))
            for freq in chord:
                seg += _sine(freq, duration_per, 0.15)
            full[pos:pos + len(seg)] += seg
            pos += len(seg)
    _write_wav(path, full)


def generate_battle(path):
    """Напряженная ритмичная композиция"""
    duration = 16.0
    full = np.zeros(int(SAMPLE_RATE * duration))
    bass_notes = [110, 110, 138.59, 138.59, 164.81, 164.81, 110, 110]
    for i, freq in enumerate(bass_notes):
        start = int(SAMPLE_RATE * i * 2.0)
        seg = _sine(freq, 0.5, 0.4)
        full[start:start + len(seg)] += seg
    lead_notes = [440, 523.25, 466.16, 392, 440, 523.25, 587.33, 466.16]
    for i, freq in enumerate(lead_notes):
        start = int(SAMPLE_RATE * i * 2.0)
        seg = _sine(freq, 1.5, 0.15)
        full[start:start + len(seg)] += seg
    _write_wav(path, full)


def init_music():
    if not PYGAME_OK:
        print("[music] pygame не установлен, музыка отключена.")
        return False
    _ensure_assets()
    calm = os.path.join(ASSETS_DIR, "calm.wav")
    battle = os.path.join(ASSETS_DIR, "battle.wav")
    if not os.path.exists(calm):
        print("[music] Генерирую calm.wav...")
        generate_calm(calm)
    if not os.path.exists(battle):
        print("[music] Генерирую battle.wav...")
        generate_battle(battle)
    try:
        pygame.mixer.init()
        return True
    except Exception as e:
        print(f"[music] Не удалось инициализировать mixer: {e}")
        return False


def play(track: str, volume: float = 0.3):
    if not PYGAME_OK:
        return
    try:
        path = os.path.join(ASSETS_DIR, f"{track}.wav")
        if not os.path.exists(path):
            return
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)
    except Exception:
        pass


def stop():
    if not PYGAME_OK:
        return
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass