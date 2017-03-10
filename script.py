import PIL
from  PIL import Image
import PIL.Image
import PIL.ImageFont
import PIL.ImageOps
import PIL.ImageDraw
import imageio
from images2gif import writeGif
from intervaltree import Interval, IntervalTree
from pytube import YouTube
from pprint import pprint
from datetime import datetime
import cv2
import math
import os
import sys
from apng import APNG
import subprocess

##### SETS OF UNICODE CHARACTERS TO USE FOR ART #####
conversorCircle = IntervalTree()
conversorCircle[0:25] = u'\u25CF'
conversorCircle[25:50] = u'\u25C9'
conversorCircle[50:75] =u'\u25D5'
conversorCircle[75:100] = u'\u25D2'
conversorCircle[100:125] = u'\u25D4'
conversorCircle[125:150] = u'\u25CE'
conversorCircle[150:175] = u'\u25F7'
conversorCircle[175:200] = u'\u25CB'
conversorCircle[200:225] = u'\u26AA'
conversorCircle[225:256] = u'\u25CC'

conversorRectangle = IntervalTree()
conversorRectangle[0:25] = u'\u2590'
conversorRectangle[25:50] = u'\u2589'
conversorRectangle[50:75] =u'\u2588'
conversorRectangle[75:100] = u'\u2587'
conversorRectangle[100:125] = u'\u2586'
conversorRectangle[125:150] = u'\u2585'
conversorRectangle[150:175] = u'\u2584'
conversorRectangle[175:200] = u'\u2583'
conversorRectangle[200:225] = u'\u2582'
conversorRectangle[225:256] = u'\u2581'

conversorSquare= IntervalTree()
conversorSquare[0:25] = u'\u25A0'    
conversorSquare[25:50] = u'\u25A9'
conversorSquare[50:75] =u'\u25A8'
conversorSquare[75:100] = u'\u25EA'
conversorSquare[100:125] = u'\u25B2'
conversorSquare[125:150] = u'\u25EB'
conversorSquare[150:175] = u'\u25A1'
conversorSquare[175:200] = u'\u25B3'
conversorSquare[200:225] = u'\u25B5'
conversorSquare[225:256] = u'\u25FD'

MAXHEIGHT = 100
PIXEL_ON = 0
PIXEL_OFF = 255

# if not os.path.exists('g/'):
#     os.makedirs(directory)

def youtube_conv(yt, name):
    print('Working on video : '+yt.filename)
    # name = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if not os.path.exists(name+'/'):
        os.makedirs(name+'/')
    yt.set_filename(name)
    video = yt.get('mp4', '360p')
    if not os.path.exists(name+'/video/'):
        os.makedirs(name+'/video/')    
    video.download(name+'/video/')
    return name

def video_to_frames(name, n_frames):
    if not os.path.exists(name+'/frames/'):
        os.makedirs(name+'/frames/')
    vidcap = cv2.VideoCapture(name+'/video/'+name+'.mp4')
    success,image = vidcap.read()
    count = 0
    frameRate = vidcap.get(3)
    while(vidcap.isOpened()):
        frameId = vidcap.get(1) #current frame number
        ret, frame = vidcap.read()
        if (ret != True):
            break
        if (frameId % int(n_frames) == 0):
            nome_file = 'frame_%03d.jpg' % count           
            print(name + '/frames/' + nome_file) 
            cv2.imwrite(name + '/frames/' + nome_file, frame)
            count += 1
    vidcap.release()
    print("Done!")

def frames_to_gray(name):
    if not os.path.exists(name+'/grayscale/'):
        os.makedirs(name+'/grayscale/')
    folder_g_path = name +'/grayscale/'
    count = 0
    for filename in os.listdir(name+'/frames/'):
        if filename == '.DS_Store':
            continue
        ficheiro = name+'/frames/'+filename
        img = Image.open(ficheiro).convert('LA')
        size = MAXHEIGHT, (MAXHEIGHT*img.size[0])/img.size[1]
        img.thumbnail(size, Image.ANTIALIAS)    
        img.save(folder_g_path + 'grayscale_%03d.png' % count)
        print(folder_g_path + 'grayscale_%03d.png' % count)
        count += 1

def gray_frames_to_txt(conversor, name):
    if not os.path.exists(name+'/textart/'):
        os.makedirs(name+'/textart/')
    folder_a_path = name+'/textart/'
    count = 0
    for filename in os.listdir(name+'/grayscale/'):
        if filename == '.DS_Store':
            continue
        f = open(folder_a_path+'text%03d.txt' % count, 'w')
        img = Image.open(name+'/grayscale/'+filename)
        pixels = list(img.getdata()) #lista de valores do tom de cinza de cada pixel
        width, height = img.size
        pixels = [pixels[i * width:(i+1) * width] for i in iter(range(height))] #criar a matriz de pixeis
        for row in pixels:
            linha = ''
            for pixel in row:
                (sett, )= conversor[pixel[0]]
                b,e,keyVal = sett 

                #adicionar 2x cada simbolo vezes pois ao utilizar esta fonte a imagem fica esticada em termos de largura
                #e assim previne que o racio l*c se altera no formato de texto
                linha = linha + keyVal + keyVal
            f.write(linha)
            f.write('\n')
        f.close()
        print(folder_a_path+'text%03d.txt' % count)
        count +=1

def txt_to_image(name):
    if not os.path.exists(name+'/imagetext/'):
        os.makedirs(name+'/imagetext/')
    folder_i_path = name+'/imagetext/'
    count = 0
    for filename in os.listdir(name+'/textart/'):
        if filename == '.DS_Store':
            continue
        image = text_image(name+'/textart/'+filename)    
        image.save(folder_i_path + 'textimage%03d.png' % count)
        print(folder_i_path + 'textimage%03d.png' % count)
        count+=1

# this part of the code was obtained from another source in order to convert the txt file to an image
# this saved me the work to do print screens on all txt files that my script generated until this point 
# this snippet comes from http://stackoverflow.com/questions/29760402/converting-a-txt-file-to-an-image-in-python
def text_image(text_path, font_path=None):
    grayscale = 'L'
    with open(text_path) as text_file:  # can throw FileNotFoundError
        lines = tuple(l.rstrip() for l in text_file.readlines())

    large_font = 20  # get better resolution with larger size
    font_path = 'everson.ttf'  # Courier New. works in windows. linux may need more explicit path
    try:
        font = PIL.ImageFont.truetype(font_path, size=large_font)
    except IOError:
        font = PIL.ImageFont.load_default()
        print('Could not use chosen font. Using default.')

    pt2px = lambda pt: int(round(pt * 96.0 / 72))  # convert points to pixels
    max_width_line = max(lines, key=lambda s: font.getsize(s)[0])

    test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    max_height = pt2px(font.getsize(test_string)[1])
    max_width = pt2px(font.getsize(max_width_line)[0])
    height = max_height * len(lines)  # perfect or a little oversized
    width = int(round(max_width + 40))  # a little oversized
    image = Image.new(grayscale, (width, height), color=PIXEL_OFF)
    draw = PIL.ImageDraw.Draw(image)

    vertical_position = 5
    horizontal_position = 5
    line_spacing = int(round(max_height * 0.8))  # reduced spacing seems better
    for line in lines:
        draw.text((horizontal_position, vertical_position),
                  line, fill=PIXEL_ON, font=font)
        vertical_position += line_spacing
    
    c_box = PIL.ImageOps.invert(image).getbbox()
    image = image.crop(c_box)
    return image

def export_movie(name, fps):
    subprocess.call('ffmpeg -framerate '+int(fps)+' -i '+ name + '/imagetext/textimage%03d.png -s:v 1280x720 -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p ' + name+ '/result.mp4' , shell=True)

def main(): 
    #arg 1 = youtube link
    #arg 2 = gap of frames between saved frames
    #arg 3 = project name
    yt = YouTube(sys.argv[1])
    n_frames = sys.argv[2]
    nome_file = sys.argv[3]
    fps = sys.argv[4]

    print('1/6 START downloading youtube video')
    proj_name = youtube_conv(yt, nome_file)
    print('1/6 COMPLETE downloading youtube video ')
    print('2/6 START converting video to frame')
    video_to_frames(proj_name, n_frames)
    print('2/6 COMPLETE converting video to frame')
    print('3/6 START converting frames to grayscale')
    frames_to_gray(proj_name)
    print('3/6 COMPLETE converting frames to grayscale')
    print('4/6 START converting frames to txt')
    gray_frames_to_txt(conversorSquare, proj_name)
    print('4/6 COMPLETE converting frames to txt')
    print('5/6 START converting frames to txt')
    txt_to_image(proj_name)
    print('5/6 COMPLETE converting frames to txt')
    print('6/6 START converting frames to txt')
    export_movie(proj_name, fps)
    print('6/6 COMPLETE converting frames to txt')

if __name__ == '__main__':
    main()