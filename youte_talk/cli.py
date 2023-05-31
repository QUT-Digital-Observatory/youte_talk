"""
Copyright: Digital Observatory 2023 <digitalobservatory@qut.edu.au>
Author: Mat Bettinson <mat.bettinson@qut.edu.au>
"""
from os import getenv
import click
from sys import exit
from youte_talk.transcriber import Transcriber

def transcribe(*args):
    trans = Transcriber(*args)
    trans.transcribe()
    print("Done!")

whispermodels = ['tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en', 'medium', 'medium.en', 'large']

@click.command()
@click.argument('url')
@click.option('--output', default=None, help="File name without an extension (extension determined by format), defaults to videoId")
@click.option("--model", type=click.Choice(whispermodels, case_sensitive=True), default="small", help="Whisper model to use (defaults to small)")
@click.option('--format', type=click.Choice(['text', 'srt', 'csv', 'json'], case_sensitive=False), default="text", help="Format of output file: text, srt or json")
@click.option("--saveaudio", is_flag=True, show_default=True, default=False, help="Save the audio stream to a webm file")
@click.option("--cpu", is_flag=True, show_default=True, default=False, help="Use the CPU instead of the GPU")
def main(url: str, output: str, model: str, format: str, saveaudio: bool, cpu: bool):
    """YouTalk: A command-line YouTube video transcriber using Whisper"""
    if not url.startswith('https://youtube.com/watch?v=') and not url.startswith('https://www.youtube.com/watch?v='):
        print("Youtube video URLs look like https://youtube.com/watch?v=...")
        exit(1)
    transcribe(url, output, model, format, saveaudio, cpu)

if __name__ == "__main__":
    main()
