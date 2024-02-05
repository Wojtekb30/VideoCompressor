print('Loading...')
print('(If the program freezes at any moment, press ENTER/RETURN to unfreeze it)')
print(" ")
import os, ffmpeg
#from pathlib import Path

def compress_video(video_full_path, output_file_name, target_size):
    os.environ['path'] = 'ffmpegprogram'
    
    # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
    min_audio_bitrate = 32000
    max_audio_bitrate = 256000
    
    probe = ffmpeg.probe(video_full_path)
    # Video duration, in s.
    duration = float(probe['format']['duration'])
    # Audio bitrate, in bps.
    audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
    # Target total bitrate, in bps.
    target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

    # Target audio bitrate, in bps
    if 10 * audio_bitrate > target_total_bitrate:
        audio_bitrate = target_total_bitrate / 10
        if audio_bitrate < min_audio_bitrate < target_total_bitrate:
            audio_bitrate = min_audio_bitrate
        elif audio_bitrate > max_audio_bitrate:
            audio_bitrate = max_audio_bitrate
    # Target video bitrate, in bps.
    video_bitrate = target_total_bitrate - audio_bitrate

    i = ffmpeg.input(video_full_path)
    ffmpeg.output(i, os.devnull,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                  ).overwrite_output().run()
    ffmpeg.output(i, output_file_name,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                  ).overwrite_output().run()

import tkinter as tk
from tkinter import filedialog
print("Welcome to video converter, which compresses MP4 videos (compressor code by 武状元 Woa, program uses FFMPEG stored in 'ffmpegprogram' folder, which is in the same directory as this program's executable file). ")
input('Press ENTER/RETURN to continue')
print(" ")
print("Choose file")
print(" ")
root = tk.Tk()
root.title("Converter")
root.withdraw()
wejscie = filedialog.askopenfilename(title='Choose video file')
rozmiar = float(input("Type new file size (in MB): "))
print("Are you sure to convert?")
input('Press ENTER/RETURN to continue')
print("Choose result file location")
wyjscie = filedialog.asksaveasfilename(filetypes=[("MP4 video","*.mp4")], defaultextension = "*.mp4")
print("Processing...")
print(repr(wejscie)[1:-1])
compress_video(repr(wejscie)[1:-1], repr(wyjscie)[1:-1], int(rozmiar * 1000))

try:
    os.remove("ffmpeg2pass-0.log")
    os.remove("ffmpeg2pass-0.log.mbtree")
    print("Deleted compressor cache.")
except:
    print("Failed to remove compressor cache.")

print("Done.")
input('Press ENTER/RETURN to end')
