from bs4 import BeautifulSoup
import urllib.request 
import requests

#get requested site
req = urllib.request.Request("https://medium.com/blog/newsletters/medium-daily-edition", headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read()

#find in soup last tag a with href and put it into variable named last
soup=BeautifulSoup(html,'html.parser')
allRef = str(soup.find_all('a',href=True,limit=10))
last = allRef.split('<a')[-1]

#get link to the newest article
newestArt= last.split('"')[3]

#find first end of header after title and get title before after last '>' sign
header=allRef.split("</h2>")[-2]
title = header.split(">")[-1]

#change to rrequest site with newest article
req = urllib.request.Request(newestArt,headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read()
soup=BeautifulSoup(html,'html.parser')

print( "text ready")
#get all text i that article
text = soup.get_text() 

import transformers
from datasets import load_dataset
import soundfile as sf
import torch

#gets summary of article
summary = transformers.pipeline("summarization", model="t5-large", tokenizer="t5-large")
answer = summary(text,min_length=100,do_sample=False)

sumArticle = answer[0]['summary_text']

print ("summary ready")

#save it as audio file
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
speaker = transformers.pipeline("text-to-speech", model="microsoft/speecht5_tts",do_sample=False)
audio = speaker(sumArticle, forward_params={"speaker_embeddings": speaker_embedding})

sf.write("audio.wav", audio["audio"], samplerate=audio["sampling_rate"])