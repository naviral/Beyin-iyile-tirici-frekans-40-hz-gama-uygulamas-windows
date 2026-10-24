"""
40 Hz Gama Beyin Dalgasi Ses Uretici (Offline MP3/WAV Generator)
Sol Kulak: 200 Hz, Sag Kulak: 240 Hz -> 40 Hz Gama Binaural Vurusu
"""
import numpy as np
import wave
import struct

def generate_gamma_wav(filename="40Hz_Gama_25Dk.wav", duration_min=25, sample_rate=44100, volume=0.35):
    duration_sec = duration_min * 60
    total_samples = int(sample_rate * duration_sec)
    
    carrier_left = 200.0
    carrier_right = 240.0
    fade_samples = int(sample_rate * 3.0)  # 3s fade in / out
    
    print(f"Uretiliyor: {filename} ({duration_min} dakika)...")
    
    with wave.open(filename, "wb") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        
        chunk_size = sample_rate * 10
        total_chunks = total_samples // chunk_size
        current_sample = 0
        
        fade_in = np.sin(np.linspace(0, np.pi/2, fade_samples))**2
        fade_out = np.sin(np.linspace(np.pi/2, 0, fade_samples))**2
        
        for c in range(total_chunks):
            t = np.arange(current_sample, current_sample + chunk_size) / sample_rate
            left = volume * np.sin(2 * np.pi * carrier_left * t)
            right = volume * np.sin(2 * np.pi * carrier_right * t)
            
            if c == 0:
                left[:fade_samples] *= fade_in
                right[:fade_samples] *= fade_in
            if c == total_chunks - 1:
                left[-fade_samples:] *= fade_out
                right[-fade_samples:] *= fade_out
                
            left_int = (left * 32767).astype(np.int16)
            right_int = (right * 32767).astype(np.int16)
            interleaved = np.empty((chunk_size * 2,), dtype=np.int16)
            interleaved[0::2] = left_int
            interleaved[1::2] = right_int
            
            wav.writeframes(interleaved.tobytes())
            current_sample += chunk_size
            
    print("Tamamlandi!")

if __name__ == "__main__":
    generate_gamma_wav()
