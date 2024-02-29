import fetch
import ai
import video

#find site with newest art list from medium
soup =fetch.findSite("https://medium.com/blog/newsletters/medium-daily-edition")

#get current newest artticle // works only for this
newestArt=fetch.findNewestArticle(soup)

#change to site with newest article // works only for this
html =fetch.findSite(newestArt[0])
title = newestArt[1]

#get all text from the article
text =fetch.getText(html)

#get summary of article
sumArt = ai.summary(text)+"like and subscribe"

#change all numbers in int format to word format
sumArt = fetch.numsToWords(sumArt)

#get 3 images with given title
ai.generateImage(title)

#Get text to speach // saved is asstes folder 
ai.textToSpeach(sumArt,"article")

#get duration of article
duration = fetch.getDuration("article")

#Get song in lenght of audio duration and add it to assets
fetch.cutWav("song","songCut",2,duration)

video.montage(duration,"image","article","songCut","combined")

video.subtitles(sumArt,8,duration)