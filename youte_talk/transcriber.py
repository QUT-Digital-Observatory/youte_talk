"""
Copyright: Digital Observatory 2023 <digitalobservatory@qut.edu.au>
Author: Mat Bettinson <mat.bettinson@qut.edu.au>
"""
from time import time
#from youtalk.scraper import makeElapsedString, getVideoDetails
from os import remove, rename
#from youtalk.whisper import whisperTranscribe
#from youtalk.parser import parse_srt
import youtube_dl

class Transcriber:
    def __init__(self, url: str, output: str, fformat: str, saveaudio: bool, apikey:str):
        """Set up a Transcription job"""
        print('url:', url)
        self.url = url
        self.output = output
        self.format = fformat
        self.saveaudio = saveaudio
        self.apikey = apikey
        self.fileext = 'txt' if fformat == 'text' else fformat

    def transcribe(self):
        return
        """Execute the transcription job, saving output as appropriate"""
        starttime = time()
        videodetails = getVideoDetails(self.url)
        print("Got metadata in", makeElapsedString(starttime, time()))
        prompt = videodetails.title + ': ' + videodetails.shortDescription # Will feed to Whisper API
        ydl_opts = {
            'format': 'worstaudio[ext=webm]',
            'outtmpl': '%(id)s.%(ext)s'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
        # <id>.webm in the current directory now
        sourcefilename = videodetails.videoId + '.webm'
        print("Downloaded in", makeElapsedString(starttime, time()))
        starttime = time()
        print("Transcribing...")
        transcript = whisperTranscribe(sourcefilename, prompt, self.apikey, self.format)
        print("Whisper transcribed in", makeElapsedString(starttime, time()))
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
     