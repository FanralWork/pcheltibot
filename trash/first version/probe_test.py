import moviepy.editor as mp
import os

video_name = [_ for _ in os.listdir() if _.endswith(".mp4") or _.endswith(".mkv")]
print(video_name)
clip = mp.VideoFileClip(video_name[0])
print("Начало сжатия")
clip.write_videofile("video_news.mp4")
print("Сжатие прошло успешно")