from moviepy import editor
from moviepy.video.tools.subtitles import SubtitlesClip
import fetch

def montage(duration,image,article,song,name):
    #get duration of 1 image
    clipLen= int(duration/3)

    clip= 3*[0]

    #add images to clipboard
    for i in range(0,3):
        clip[i] = editor.ImageClip(f"assets/{image}{i}.png").subclip(clipLen*(i),clipLen*(i+1))

    clip[0].fps=24
    #get audio song and voicedover article
    article = editor.AudioFileClip(f"assets/{article}.wav").fx(editor.afx.volumex,0.5)
    song = editor.AudioFileClip(f"assets/{song}.wav").fx(editor.afx.volumex,0.05)

    #combine clips
    combined = editor.concatenate_videoclips(clips=clip)

    #combine audio
    combined.audio = editor.CompositeAudioClip([article,song])

    #save
    combined.write_videofile(f"assets/{name}.mp4")


def subtitles(text,lenParagraph,duration):
    #creates parameters for all text
    generator = lambda txt: editor.TextClip(txt, font='Arial', fontsize=120,method="caption", color='white',kerning=2,interline=1,size=(1080,1920))

    #timestamps of lasting of text and given text
    # [ ((start,end),subtitle)]
    subs = []
    text = fetch.splitText(text,lenParagraph)

    interval=duration/len(text)

    for i in range(0,len(text)):
        subs.append(((int(i*interval),int((i+1)*interval)),text[i]))
    #give font etc to all text
    subtitles = SubtitlesClip(subs, generator)

    #put tougether video with subtitles
    video = editor.VideoFileClip("assets/combined.mp4")
    result = editor.CompositeVideoClip([video, subtitles.set_position(('center'))])

    #save
    result.write_videofile("assets/combinedTitled.mp4")