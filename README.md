# Requirements
  ffmpeg
  pip install -r requirements.txt
  everson mono.tff
  
# How to run it

python3 script.py arg1 arg2 arg3 arg4 arg5

* arg 1 = youtube link (e.g https://www.youtube.com/watch?v=dQw4w9WgXcQ)
* arg 2 = gap of frames between saved frames (e.g 2, this will record frame0, frame2, frame4, etc...)
* arg 3 = project name (name you want to give to the resulting project)
* arg 4 = fps for mp4 render (frames per second you want when rendering the video)
* arg 5 = conversion characters (circle, square, rectangle)

arg 5  
circle    -> ◌,○,◷,◎,◔,◒,◕,◉,●  
rectangle -> ▁,▂,▃,▄,▅,▆,▇,█,▉  
square    -> ◽︎,▵,△,□,◫,▲,◪,▨,▩  


# Steps

* convert youtube video to mp4
* convert the video to frames
* convert the frames to grayscale frames
* convert the grayscale frames to uniscode art in txt
* convert the txt file to a png (disclaimer: this part was found on the internet so I didn't have to screenshot all the txt files in order to generate the final video, it was just a simple shortcut that doesn't modify the core part of the script written by me)
* render video based on the resulting pngs


# Example

On the folder example you'll find a conversion from a youtube video (trainspotting intro - https://www.youtube.com/watch?v=glEAxaXbAM0) into a video composed by unicode art frames with the "circle" characters.

python3 script.py https://www.youtube.com/watch?v=glEAxaXbAM0 2 2 10 circle
