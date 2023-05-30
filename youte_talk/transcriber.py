"""
Copyright: Digital Observatory 2023 <digitalobservatory@qut.edu.au>
Author: Mat Bettinson <mat.bettinson@qut.edu.au>
"""
from time import time
from youte_talk.scraper import get_VideoDetails
from os import remove, rename
from youte_talk.whisper import whisper_transcribe
#from youtalk.parser import parse_srt
import youtube_dl
from datetime import timedelta

class Transcriber:
    def __init__(self, url: str, output: str, fformat: str, saveaudio: bool):
        """Set up a Transcription job"""
        print('url:', url)
        self.url = url
        self.output = output
        self.format = fformat
        self.saveaudio = saveaudio
        self.fileext = 'txt' if fformat == 'text' else fformat

    def get_elapsed(self, start: float, end: float) -> str:
        return str(timedelta(seconds=round(end-start)))

    def transcribe(self):
        """Execute the transcription job, saving output as appropriate"""
        starttime = time()
        videodetails = get_VideoDetails(self.url)
        if videodetails is None:
            print("Failed to get video details")
            return
        print("Got metadata in", self.get_elapsed(starttime, time()))
        prompt = videodetails.title + ': ' + videodetails.shortDescription # Will feed to Whisper API
        ydl_opts = {
            'format': 'worstaudio[ext=webm]',
            'outtmpl': '%(id)s.%(ext)s'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
        # <id>.webm in the current directory now
        sourcefilename = videodetails.videoId + '.webm'
        print("Downloaded in", self.get_elapsed(starttime, time()))
        starttime = time()
        print("Transcribing...")
        transcript = whisper_transcribe(sourcefilename, prompt, self.format)
        print("Whisper transcribed in", self.get_elapsed(starttime, time()))
        outputfilename = self.output + '.' + self.fileext
        outputdata = transcript # Use plain text if output is srt or text
        if self.format == 'json':
            caption = parse_srt(transcript) # Otherwise use the parsed SRT
            outputdata = caption.json() # And use the json serialised format for it
        with open(outputfilename, 'w') as f:
            f.write(outputdata)
        # clean up
        if self.saveaudio:
            outfile = self.output + '.webm'
            if sourcefilename != outfile:
                rename(sourcefilename, outfile)
        else:
            remove(sourcefilename)
     