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

There's also the option of running Whisper on a CPU. This is much slower, but this doesn't require a GPU at all and is quite useful if you have insufficient memory to run a larger model. Modern systems can still transcribe at better than real-time even with the large model. Some examples drawn on an Intel i7-12700 laptop and a 4GB Nvidia RTX 3050 GPU transcribing a short 4 minute video:

* CPU, small model: 0m 46s
* GPU, small model: 0m 16s
* CPU, medium model: 2m 3s
* CPU, large model: 3m 30s

Note, you can always try to transcribe a video with a larger model on GPU, and if it fails due to memory constraints, just re-run the command with the `--cpu` switch.

## Installing

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
