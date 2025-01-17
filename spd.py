from pyannote.audio import Pipeline
from pydub import AudioSegment
import whisper
import numpy as np
import gc
import torch

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization", use_auth_token="register to huggingface website to get the access token")


def read(k):
    y = np.array(k.get_array_of_samples())
    return np.float32(y) / 32768


def millisec(timeStr):
    timeStr = timeStr.replace(']', '')
    spl = timeStr.split(":")
    return (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2])) * 1000)


k = str(pipeline(
    "audio.mp3")).split('\n')

del pipeline
gc.collect()

audio = AudioSegment.from_mp3(
    "audio.mp3")
audio = audio.set_frame_rate(16000)

device = torch.device('cuda')
model = whisper.load_model("small.en", device=device)

for l in range(len(k)):

    j = k[l].split(" ")
    start = int(millisec(j[1]))
    end = int(millisec(j[4]))

    tr = read(audio[start:end])

    result = model.transcribe(tr, fp16=False)

    f = open("tr_file.txt", "a")
    f.write(f'\n[ {j[1]} -- {j[4]} ] {j[6]} : {result["text"]}')
    f.close()

    del f
    del result
    del tr
    del j
    gc.collect()
