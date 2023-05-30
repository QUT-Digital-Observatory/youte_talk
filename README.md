# YouTalk: a tool for transcribing YouTube videos

YouTalk is a simple command line program for transcribing YouTube videos. That is, it downloads the audio from a YouTube video and produces a transcript in a variety of formats including plain text, time-stamped SRT text caption format, JSON and CSV.

## Why YouTalk?

There is a need for high quality automatic transcription of YouTube videos, particularly for research use cases. 
This can be accomplished by some tools which download the subtitle captions from YouTube. That's fine if the video has been captioned professionally, but that is not usually available for user-generated content. 

YouTube has automatic subtitles, but uploaders need to enable this feature. The quality of automatic captions is low compared to state-of-the-art for speech to text systems. This means transcripts need substantial editing to be useful.

YouTalk uses [youtube-dl](https://github.com/ytdl-org/youtube-dl) to download the audio from a YouTube video. It then uses the [Whisper](https://github.com/openai/whisper) speech recognition system from OpenAI to produce a transcript. Whisper is is a state-of-the-art speech to text system that achieves results comparable with human transcribers. See [paper](https://arxiv.org/abs/2212.04356). 

## Installing

YouTalk requires Python 3.10 or later. It is recommended to use a virtual environment.

`pip install youte-text`

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

