"""
Copyright: Digital Observatory 2023 <digitalobservatory@qut.edu.au>
Author: Mat Bettinson <mat.bettinson@qut.edu.au>
"""
from __future__ import annotations

import os
import subprocess
import warnings
from sys import exit

import click

warnings.filterwarnings("ignore", message=".*The 'nopython' keyword.*")
warnings.filterwarnings("ignore", message=".*FP16 is not supported on CPU.*")
warnings.filterwarnings(
    "ignore", message=".*Performing inference on CPU when CUDA is available.*"
)


def transcribe(*args):
    from youte_talk.transcriber import Transcriber

    trans = Transcriber(*args)
    trans.transcribe()
    click.echo("Done!")


def is_ffmpeg_available():
    try:
        # The "which" command is used to find out if a system command exists.
        # It's used here to check if ffmpeg is available.
        # This works on Unix/Linux/Mac systems. On Windows, it's "where".
        command = "where" if os.name == "nt" else "which"
        subprocess.check_output([command, "ffmpeg"])
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


whispermodels = [
    "tiny",
    "tiny.en",
    "base",
    "base.en",
    "small",
    "small.en",
    "medium",
    "medium.en",
    "large",
]


@click.command()
@click.argument("url")
@click.option(
    "--output",
    default=None,
    help="File name without an extension (extension determined by format), defaults to videoId",
)
@click.option(
    "--model",
    type=click.Choice(whispermodels, case_sensitive=True),
    default="small",
    help="Whisper model to use",
    show_default=True,
)
@click.option(
    "--format",
    type=click.Choice(["text", "srt", "csv", "json"], case_sensitive=False),
    default="text",
    help="Format of output file: text, srt or json",
    show_default=True,
)
@click.option(
    "--saveaudio",
    is_flag=True,
    default=False,
    help="Save the audio stream to a webm file",
)
@click.option(
    "--cpu",
    is_flag=True,
    default=False,
    help="Use the CPU instead of the GPU",
)
def main(url: str, output: str, model: str, format: str, saveaudio: bool, cpu: bool):
    """YouTalk: A command-line YouTube video transcriber using Whisper"""
    if not url.startswith("https://youtube.com/watch?v=") and not url.startswith(
        "https://www.youtube.com/watch?v="
    ):
        raise click.BadArgumentUsage(
            "YouTube video URLs must look like https://youtube.com/watch?v=..."
        )

    if not is_ffmpeg_available():
        click.echo(
            "\nYoute_Talk requires ffmpeg but it is not available!\n"
            " - See https://ffmpeg.org/download.html for installation instructions\n"
            " - On Windows, you may need to add ffmpeg to your PATH\n"
            " - On Linux, you may need to install ffmpeg with your package manager\n"
        )
        raise click.Abort

    transcribe(url, output, model, format, saveaudio, cpu)


if __name__ == "__main__":
    main()
