import sys
import color_ascii_art_generator
import cv2
import textfile_editor
import os
import fpstimer
import colorama
import time
import threading
import ffmpeg
import winsound
import reprint


#if u use command , it should be like this
#python src//test_mp4_player.py


ascii_output_path = "Ascii frames"
frame_output_path = "Image frames"
fps = 0
cap = None
total_frame = 0
height = 0
width = 0
ASCII_LIST = []
REPRINT = reprint.Reprint()


def set_up(mp4_path: str, new_width: int):
    global cap
    global fps
    global total_frame
    global height
    global width
    cap = cv2.VideoCapture(mp4_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    ret, frame = cap.read()
    new_height, new_width, channels = frame.shape[:3]
    height = new_height
    width = new_width
    output_mp4_frame(mp4_path)
    output_color_ascii_txt_by_mp4_frame(new_width)
    convert_mp4_to_mp3(mp4_path)
    set_ascii_frame(mp4_path, new_width)



def play_video_and_sound():
    thread1 = threading.Thread(target=play_mp3).start()
    play_mp4()  


def set_ascii_frame(mp4_path: str, width: int):
    now = 0
    while(total_frame > now):
        frame = textfile_editor.read_txt_file(
            f"{ascii_output_path}\color_ascii_frame{now}.txt")
        ASCII_LIST.append(frame)
        progress_bar(now + 1, total_frame)
        now += 1


def convert_mp4_to_mp3(path: str):
    if not os.path.isfile("audio.wav"):
        video = ffmpeg.input(path)
        audio = video.audio
        stream = ffmpeg.output(audio, "audio.wav")
        ffmpeg.run(stream)


def play_mp3():
    winsound.PlaySound("audio.wav", winsound.SND_ASYNC | winsound.SND_ALIAS)


#######################################
# Output image list   function = output_mp4_frame(mp4path)
#######################################
def output_mp4_frame(mp4_path):
    if(59 < fps < 61):
        output_10fps_video_by_30fps_or_60fps_video(mp4_path, True)
    if(29 < fps < 31):
        output_10fps_video_by_30fps_or_60fps_video(mp4_path, False)
    else:
        print("Error : this video is not 60 or 30 fps video")


def output_image(output_path: str, image):
    if not os.path.isfile(output_path):
        cv2.imwrite(output_path, image)


def output_10fps_video_by_30fps_or_60fps_video(mp4_path: str, is60fps: bool):
    num = 0
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    while(num < length):
        is_image, frame_img = cap.read()
        if(is60fps):
            if(num % 6 == 0):
                output_image(
                    f"{frame_output_path}\image_frame{num}.jpg", frame_img)
        else:
            if(num % 3 == 0):
                output_image(
                    f"{frame_output_path}\image_frame{num}.jpg", frame_img)
        num += 1
        progress_bar(num + 1, length)


#######################################
# Output color ascii frame list   function = output_mp4_frame(mp4path)
#######################################

def output_color_ascii_txt_by_mp4_frame(width: int):
    num = 0
    total_frame
    while(total_frame > num):
        image = cv2.imread(f"{frame_output_path}\image_frame{num}.jpg")
        output_path = f"{ascii_output_path}\color_ascii_frame{num}.txt"
        color_ascii_art_generator.output_ascii_image_as_txt_file(image, output_path, width)
        progress_bar(num + 1, total_frame)
        num += 1



def play_mp4():
    now = 0
    fps_timer = fpstimer.FPSTimer(10)
    os.system(f'mode {width}, {height}')
    while(now < total_frame):
        lines = ASCII_LIST[now].split("\n")
        REPRINT.do(lines)
        now += 1
        fps_timer.sleep()


def progress_bar(current, total, barLength=25):
    progress = float(current) * 100 / total
    arrow = '#' * int(progress / 100 * barLength - 1)
    spaces = ' ' * (barLength - len(arrow))
    sys.stdout.write('\rProgress: [%s%s] %d%% Frame %d of %d frames' % (arrow, spaces, progress, current, total))


mp4_path = r""
set_up(mp4_path, 100)
play_video_and_sound()
