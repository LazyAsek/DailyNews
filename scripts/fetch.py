from bs4 import BeautifulSoup
import urllib.request 
import inflect
from scipy.io import wavfile
import math
from PIL import Image

#get requested site
def findSite(link):
    req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    html= urllib.request.urlopen(req).read()
    return BeautifulSoup(html,'html.parser')

#find in soup last tag a with href and put it into variable named last
def findNewestArticle(soup):
    allRef = str(soup.find_all('a',href=True,limit=10))

    #get link to the newest article
    last = allRef.split('<a')[-1]

    #find first end of header after title and get title before after last '>' sign
    header=allRef.split("</h2>")[-2]
    title = header.split(">")[-1]

    return (last.split('"')[3],title)

#get all text from site
def getText(soup):
    print( "text ready")
    return soup.get_text() 

#find numbers and change them to words
def numsToWords(text):

    finalText=""
    count=0
    num=""

    for pos in range(0,len(text)):
        #check if there is need to skip a line( edge case when number is last returning wrong result )
        if count == 1:count-=1
        if count !=0 :
            count-=1
            continue
        try:
            #getting whole number until find non number
            while(True):
                number=int(text[pos+count])
                num+=str(number)
                count+=1
        except:
            #change % to named and skip a loop once
            if text[pos]=="%":
                finalText+=" percent"
                continue

            #if number found transfer it to words
            if count != 0 :
                num = inflect.engine().number_to_words(int(num))
                finalText+=num
                num=""

            #no number found just add next
            else:
                finalText+=text[pos]
    print("changes ready")
    return finalText

def cutWav(orginal, name, start, end):
    # Read the WAV file
    sample_rate, data = wavfile.read(f"assets/{orginal}.wav")
    
    # Convert start and end times to sample indices
    start = int(start * sample_rate)
    end = int(end * sample_rate)
    
    # Slice the audio data
    cut_data = data[start:end]
    
    # Write the sliced data to a new WAV file
    wavfile.write(f"assets/{name}.wav", sample_rate, cut_data)

def getDuration(name):
    #getting duration of wav file
    (rate,sig)=wavfile.read(f"assets/{name}.wav")
    return math.ceil(len(sig)/float(rate))

def scaleimage(name):
    #scale image to shorts format from provided image
    im = Image.open(f"assets/{name}.png")
    im = im.resize((2048, 2048))
    imm = im.crop((484,0,1564,1920))
    imm.save(f"assets/{name}.png")

def splitText(text,size):
    words= text.split()
    finnished=[]
    bunch=""
    count=0
    for w in words:
        if count != size:
            bunch+=" "+w
            count+=1
        else:
            finnished.append(bunch)
            bunch=""
            count=0
    return finnished