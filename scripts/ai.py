import transformers
import torch
from scipy.io.wavfile import write

#gets summary of article
def summary(text):
    summary = transformers.pipeline("summarization", model="t5-large", tokenizer="t5-large")
    answer = summary(text,min_length=100,do_sample=False)

    print ("summary ready")
    return answer[0]['summary_text']

#text to speach magic
def textToSpeach(text,name):
    model = transformers.VitsModel.from_pretrained("facebook/mms-tts-eng")
    tokenizer =transformers.AutoTokenizer.from_pretrained("facebook/mms-tts-eng")

    inputs=tokenizer(text,return_tensors="pt")

    with torch.no_grad():
        output = model(**inputs).waveform
    write(f"{name}.wav", rate=model.config.sampling_rate, data=output.float().numpy().T)
    print("Text to speach ready")