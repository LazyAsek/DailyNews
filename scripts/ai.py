import transformers
import torch
from scipy.io import wavfile
import math
from diffusers import DiffusionPipeline
from PIL import Image
#gets summary of article
def summary(text):
    summary = transformers.pipeline("summarization", model="t5-large", tokenizer="t5-large")
    answer = summary(text,min_length=100,do_sample=False)

    print ("summary ready")
    return answer[0]['summary_text']

#text to speach magic
def textToSpeach(text,name):
    print("started tts")
    #disable training request
    transformers.logging.set_verbosity_error()

    #load model and tokenaizer
    model = transformers.VitsModel.from_pretrained("facebook/mms-tts-eng")
    tokenizer =transformers.AutoTokenizer.from_pretrained("facebook/mms-tts-eng")

    inputs=tokenizer(text,return_tensors="pt")

    #saveing it as a wav file
    with torch.no_grad():
        output = model(**inputs).waveform
    wavfile.write(f"assets/{name}.wav", rate=model.config.sampling_rate, data=output.float().numpy().T)
    print("Text to speach ready")


def generateImage(prompt):
    #pick model for generation
    pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
    pipe.to("cuda")

    #loop to generate and save images
    for i in range(0,3):
        images = pipe(prompt=prompt).images[0]
        images.save(f"assets/image{i}.png")
