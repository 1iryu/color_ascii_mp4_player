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
import keyboard


# if u use command , it should be like this
# python src//test_mp4_player.py

ascii_output_path = "Ascii frames"
frame_output_path = "Image frames"
fps = 0
cap = None
total_frame = 0
height = 0
width = 0
resize = False
ASCII_LIST = []
REPRINT = reprint.Reprint()


def set_up(mp4_path: str, is_resize: bool, new_height : int = 0 ,new_width: int = 0):
    global cap
    global fps
    global total_frame
    global height
    global width
    global resize
    cap = cv2.VideoCapture(mp4_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    height = new_height
    width = new_width
    resize = is_resize
    print(height)
    print(width)
    make_color_ascii_video(mp4_path)

# mp4 -> mp3
# mp4 -> output image -> output color ascii image -> set color ascii mp4 in variables


def make_color_ascii_video(mp4_path: str):
    output_mp4_frame(mp4_path, resize)
    output_color_ascii_txt_by_mp4_frame()
    convert_mp4_to_mp3(mp4_path)
    set_ascii_frame(mp4_path)


def set_ascii_frame(mp4_path: str):
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


#######################################
# Output image list   function = output_mp4_frame(mp4path)
#######################################
def output_mp4_frame(mp4_path: str, resize: bool):
    print(resize)
    if(59 < fps < 61):
        output_10fps_video_by_30fps_or_60fps_video(mp4_path, True, resize)
    if(29 < fps < 31):
        output_10fps_video_by_30fps_or_60fps_video(mp4_path, False, resize)
    else:
        print("Error : this video is not 60 or 30 fps video")


def output_image(output_path: str, image):
    if not os.path.isfile(output_path):
        cv2.imwrite(output_path, image)


def output_10fps_video_by_30fps_or_60fps_video(mp4_path: str, is60fps: bool, resize: bool):
    num = 0
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    while(num < length):
        is_image, frame_img = cap.read()
        if(is60fps):
            if(num % 6 == 0):
                if(resize):
                    frame_img = resize_image(frame_img, width, height)
                output_image(f"{frame_output_path}\image_frame{num}.jpg", frame_img)
        else:
            if(num % 3 == 0):
                if(resize):
                    frame_img = resize_image(frame_img, width, height)
                output_image(f"{frame_output_path}\image_frame{num}.jpg", frame_img)
        num += 1
        progress_bar(num + 1, length)


def resize_image(image, new_width, new_height):
    frame = cv2.resize(image, (new_width, new_height))
    return frame


# def resize_image(image, new_width):
#     height, width, ch_count = image.shape
#     ratio = (height / float(width * 2.5))
#     new_height = int(new_width * ratio)
#     frame = cv2.resize(image, (new_width, new_height))
#     return frame


#######################################
# Output color ascii frame list   function = output_mp4_frame(mp4path)
#######################################

def output_color_ascii_txt_by_mp4_frame():
    num = 0
    total_frame
    while(total_frame > num):
        image = cv2.imread(f"{frame_output_path}\image_frame{num}.jpg")
        if image is not None:
            output_path = f"{ascii_output_path}\color_ascii_frame{num}.txt"
            color_ascii_art_generator.output_ascii_image_as_txt_file(image, output_path)
        progress_bar(num + 1, total_frame)
        num += 1


#######################################
# play video   function = play_video()
#######################################
def play_video():
    thread1 = threading.Thread(target=play_mp3).start()
    play_color_ascii_mp4()


def play_color_ascii_mp4():
    full_screen()
    now = 0
    fps_timer = fpstimer.FPSTimer(10)
    os.system(f'mode {width}, {height}')
    while(now < total_frame):
        print(ASCII_LIST[now])
        now += 1
        fps_timer.sleep()


def full_screen():
    keyboard.press('f11')



def play_mp3():
    winsound.PlaySound("audio.wav", winsound.SND_ASYNC | winsound.SND_ALIAS)


def progress_bar(current, total, barLength=25):
    progress = float(current) * 100 / total
    arrow = '#' * int(progress / 100 * barLength - 1)
    spaces = ' ' * (barLength - len(arrow))
    sys.stdout.write('\rProgress: [%s%s] %d%% Frame %d of %d frames' % (
        arrow, spaces, progress, current, total))

#w 274 h 77