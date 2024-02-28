import fetch
import ai

#find site with newest art list from medium
soup =fetch.findSite("https://medium.com/blog/newsletters/medium-daily-edition")

#get current newest artticle
newestArt=fetch.findNewestArticle(soup)

#change to site with newest article
html =fetch.findSite(newestArt[0])

#get all text from the article
text =fetch.getText(html)

#get summary of article
sumArt = ai.summary(text)

sumArt = fetch.numsToWords(sumArt)

#Get text to speach
ai.textToSpeach(sumArt,"article")