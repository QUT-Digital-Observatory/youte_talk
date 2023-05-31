# Youte_talk: a tool for transcribing YouTube videos

Youte_talk, or YouTalk for short, is a simple command line program for transcribing YouTube videos. That is, it downloads the audio from a YouTube video and produces a transcript in a variety of formats including plain text, time-stamped SRT text caption format, JSON and CSV. It is a member of the [Youte](https://github.com/QUT-Digital-Observatory/youte) family of tools for working with YouTube data.

## Why YouTalk?

There is a need for high quality automatic transcription of YouTube videos, particularly for research use cases. 
This can be accomplished by some tools which download the subtitle captions from YouTube. That's fine if the video has been captioned professionally, but that is not usually available for user-generated content. 

YouTube has automatic subtitles, but uploaders need to enable this feature. The quality of automatic captions is low compared to state-of-the-art for speech to text systems. This means transcripts need substantial editing to be useful.

YouTalk uses [youtube-dl](https://github.com/ytdl-org/youtube-dl) to download the audio from a YouTube video. It then uses the [Whisper](https://github.com/openai/whisper) speech recognition system from OpenAI to produce a transcript. Whisper is is a state-of-the-art speech to text system that achieves results comparable with human transcribers. See [paper](https://arxiv.org/abs/2212.04356). 

## Installing

YouTalk requires Python 3.10 or later. It is recommended to use a virtual environment.

`pip install youte-text`

Please note: YouTalk's Whisper dependency includes a PyTorch installation which is very large and takes a while to install. This is unfortunately the norm for GPU compute tools, even if you're only going to use the CPU.

An ffmpeg installation is also required.

* On Windows see https://ffmpeg.org/download.html
* On Mac, `brew install ffmpeg`
* On Linux, `sudo apt install ffmpeg` or similar depending on your package manager

## Usage

After installing, you can run `youtalk` from the command line. You must provide a YouTube URL. You can also specify the output format, the output file name, and the Whisper model to use. The default is to use the small model and output a text file with the same name as the video ID.

```
Usage: youtalk [OPTIONS] URL

  YouTalk: A command-line YouTube video transcriber using Whisper

Options:
  --output TEXT                   File name without an extension (extension
                                  determined by format), defaults to videoId
  --model [tiny|tiny.en|base|base.en|small|small.en|medium|medium.en|large]
                                  Whisper model to use (defaults to small)
  --format [text|srt|csv|json]    Format of output file: text, srt or json
  --saveaudio                     Save the audio stream to a webm file
  --cpu                           Use the CPU instead of the GPU
  --help                          Show this message and exit.
```

Note, if using the --saveaudio switch, the audio file will be saved in the current working directory with the name `videoId.webm`.
If you run YouTalk again on the same video, it will not download the audio again, but will use the existing file.

Note: The webm files served by YouTube are encoded with the [Opus](https://opus-codec.org/) codec, Youte_Talk saves the stream without transcoding. Opus has excellent low-bitrate performance for speech.

## Whisper and performance

YouTalk uses a local installation of Whisper which is free and does not require an API key. 
On first run, Whisper will download a language model. YouTalk defaults to using the 'small' multi-lingual model with a model size of around 250MB, and requiring around 2GB of VRAM on a modern GPU.

Models with a .en suffix are English only and perform better than the multilingual variants. The difference between English and multi-lingual variants is less apparent for the larger models.

Larger models are more accurate but are much slower, and are unlikely to fit on common GPUs. See the [table](https://github.com/openai/whisper) on the Whisper README for model sizes and relative performance.

There's also the option of running Whisper on a CPU. This is much slower, but this doesn't require a GPU at all and is quite useful if you have insufficient memory to run a larger model. Modern systems can still transcribe at better than real-time even with the large model. Some examples drawn on an Intel i7-12700 laptop and a 4GB Nvidia RTX 3050 GPU transcribing a short 4 minute video:

* CPU, small model: 0m 46s
* GPU, small model: 0m 16s
* CPU, medium model: 2m 3s
* CPU, large model: 3m 30s

Note, you can always try on the GPU first, and if it fails due to memory constraints (you will see a cuda memory allocation error), just re-run the command with the `--cpu` switch.

## Installing from Git (for dev etc)

- `git clone https://github.com/QUT-Digital-Observatory/youte_talk.git`
- `cd youte_talk`
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -e .`

## Using as a Python module

You can also use YouTalk as a module. The main function is `youtalk.transcribe` which takes a YouTube URL and returns a transcript as a string. You can also specify the output format and the model to use. For example:

To transcribe a video and save the output to a file called `transcript.txt`:

```python:
from youte_talk.transcriber import Transcriber

transcriber = Transcriber('https://www.youtube.com/watch?v=9bZkp7q19f0', output='transcript', model='small')
transcriber.transcribe()
```

To transcribe an audio file with the CPU and retrieve a list of Segment dataclasses:

```python:
from youte_talk.whisper import WhisperTranscribe

whisper = WhisperTranscribe('filename.webm', prompt = 'A meeting transcript', cpu = True)
for segment in whisper.segments:
    print(segment.start,':', segment.text)
```

The WhisperTranscribe class also returns strings in various formats as .text, srt, .csv and .json properties.


