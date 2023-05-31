import whisper
from dataclasses import dataclass
from typing import TypedDict
import json
import csv
import io
from datetime import timedelta
from torch.cuda import is_available

# How hard was that OpenAI? Types. It's not hard.
class WhisperSegment(TypedDict):
    id: int
    seek: int
    start: int
    end: int
    text: str
    tokens: list[int]
    temperature: float
    avg_logprob: float
    compression_ratio: float
    no_speech_prob: float

@dataclass
class Segment:
    id: int
    start: int
    end: int
    text: str

class WhisperTranscribe:
    def __init__(self, sourcefile: str, prompt: str | None = None, modelname: str = "small", cpu: bool = False):
        self.segmentlist = []
        if cpu == False and is_available() == False:
            print("CUDA is not available. Falling back to CPU.")
            cpu = True
        model = whisper.load_model(modelname, device='cpu' if cpu else 'cuda')
        # This doesn't return what OpenAI says it does
        result = model.transcribe(sourcefile, initial_prompt=prompt)
        # It returns a dict, and we will store the verbose segments structure
        self.segmentlist: list[WhisperSegment] = result['segments'] # type: ignore

    @property
    def text(self) -> str:
        return ''.join([segment['text'] for segment in self.segmentlist])
    
    @property
    def json(self) -> str:
        objlist = []
        for segment in self.segmentlist:
            objlist.append({
                'id': segment['id'],
                'start': round(segment['start'], 2),
                'end': round(segment['end'], 2),
                'text': segment['text'].strip()
            })
        return json.dumps(objlist, indent=2)
    
    @property
    def segments(self) -> list[Segment]:
        short_segments = []
        for segment in self.segmentlist:
            short_segments.append(Segment(
                id=segment['id'],
                start=round(segment['start'], 2),
                end=round(segment['end'], 2),
                text=segment['text'].strip()
            ))
        return short_segments
    
    @property
    def csv(self) -> str | None:
        try:
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=['id', 'start', 'end', 'text'], quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for segment in self.segmentlist:
                seg = {
                    'id': segment['id'],
                    'start': round(segment['start'], 2),
                    'end': round(segment['end'], 2),
                    'text': segment['text'].strip()
                }
                # encode special characters in the 'text' field
                seg['text'] = seg['text'].encode('unicode_escape').decode('utf-8')
                writer.writerow(seg)
            return output.getvalue()
        except Exception as e:
            print("An error occurred while creating the CSV string.")
            print(str(e))
            return None
        
    @property
    def srt(self) -> str:
        srt_str = ""

        for i, segment in enumerate(self.segmentlist):
            # Convert start and end times to hh:mm:ss,sss format
            start_time = timedelta(seconds=segment['start'])
            end_time = timedelta(seconds=segment['end'])

            # Convert timedelta to appropriate string format
            str_start_time = str(start_time).zfill(8)
            if '.' in str_start_time:
                str_start_time = str_start_time.replace('.', ',')
                if len(str_start_time.split(',')[1]) < 3:
                    str_start_time = str_start_time + '0'*(3-len(str_start_time.split(',')[1]))
            else:
                str_start_time = str_start_time + ',000'

            str_end_time = str(end_time).zfill(8)
            if '.' in str_end_time:
                str_end_time = str_end_time.replace('.', ',')
                if len(str_end_time.split(',')[1]) < 3:
                    str_end_time = str_end_time + '0'*(3-len(str_end_time.split(',')[1]))
            else:
                str_end_time = str_end_time + ',000'

            # Add index, time range, and text to the string
            srt_str += f"{i+1}\n{str_start_time} --> {str_end_time}\n{segment['text'].strip()}\n\n"

        return srt_str
