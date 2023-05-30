# YouTalk: a command-line tool to transcribe YouTube videos

YouTalk is a simple command line program for transcribing YouTube videos. 
YouTube has built-in support for video subtitles but it is not always available, and the quality of the automatic subtitles is far short of the state-of-the-art for speech to text systems.

YouTalk uses [youtube-dl](https://github.com/ytdl-org/youtube-dl) to download the audio from a YouTube video. It then uses [Whisper](https://github.com/openai/whisper) speech recognition system from OpenAI to produce a transcript. This is a large model that is trained on a large corpus of audio data which achieves results comparable with human transcribers. See [paper](https://arxiv.org/abs/2212.04356).

Depending on the output desired, YouTalk may transform the text output of Whisper into a CSV or JSON file.


## Whisper and performance

OpenAI offer Whisper as a cloud service. This costs money and requires an API key. YouTalk uses a local installation of Whisper which is free and does not require an API key. Additionally, the cloud service leaks data between sessions, e.g. you may receive parts of someone elses' transcript. 

The down side is that Whisper requires a fair volume of disk space, is computationally expensive, and is not particularly fast. It benefits greatly from a GPU, but does not require one.

On first run, Whisper will download a language model. YouTalk defaults to using the 'small' multi-lingual model with a model size of around 250MB, and requiring around 2GB of VRAM on a GPU. 
The size of the model affects the accuracy and resource consumption. Larger models are dramatically slower, but have smaller improvements in accuracy. See the [table](https://github.com/openai/whisper) on the Whisper README for model sizes and relative performance.

## Installing



## Leftovers

[label](uCqI2o6pKeM.txt)

'https://www.youtube.com/watch?v=uCqI2o6pKeM'

pip install --upgrade --force-reinstall git+https://github.com/ytdl-org/youtube-dl.git

pip install git+https://github.com/openai/whisper.git 
