from bs4 import BeautifulSoup
import urllib.request 
import inflect

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
    return finalText