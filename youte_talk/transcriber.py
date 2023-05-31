"""
Copyright: Digital Observatory 2023 <digitalobservatory@qut.edu.au>
Author: Mat Bettinson <mat.bettinson@qut.edu.au>
"""
from time import time
from youte_talk.scraper import get_VideoDetails
from os import remove, rename, path
from youte_talk.whisper import WhisperTranscribe
#from youtalk.parser import parse_srt
import youtube_dl
from datetime import timedelta

class Transcriber:
    def __init__(self, url: str, output: str | None = None, model: str = 'small', fformat: str = 'small', saveaudio: bool = False, cpu: bool = False):
        """Set up a Transcription job"""
        print('url:', url)
        self.url = url
        self.output = url.split('=')[-1] if output is None else output 
        self.model = model
        self.format = fformat
        self.saveaudio = saveaudio
        self.fileext = 'txt' if fformat == 'text' else fformat
        self.cpu = cpu

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
        sourcefilename = videodetails.videoId + '.webm'
        if not path.isfile(sourcefilename):
            starttime = time()
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            print("Downloaded in", self.get_elapsed(starttime, time()))
        # <id>.webm in the current directory now
        starttime = time()
        print("Transcribing...")
        transcription = WhisperTranscribe(sourcefilename, prompt, self.model, self.cpu)
        print("Whisper transcribed in", self.get_elapsed(starttime, time()))
        outputfilename = self.output + '.' + self.fileext
        outputdata = None
        match self.format:
            case 'text':
                outputdata = transcription.text
            case 'srt':
                outputdata = transcription.srt
            case 'json':
                outputdata = transcription.json
            case 'csv':
                outputdata = transcription.csv
        assert outputdata is not None
        with open(outputfilename, 'w') as f:
            f.write(outputdata)
        # clean up
        if self.saveaudio:
            outfile = self.output + '.webm'
            if sourcefilename != outfile:
                rename(sourcefilename, outfile)
        else:
            remove(sourcefilename)
     