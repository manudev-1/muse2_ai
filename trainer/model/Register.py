import os
import json
import time
from datetime import datetime
from threading import Lock
from typing import Literal

from model.EEG.Reader import Reader
from log.__print import print

class Register:
    def __init__(self, output_path: str = "dataset/"):
        self.reader = Reader()
        self.output_path = output_path
        os.makedirs(self.output_path, exist_ok=True)
        
        self.lock = Lock()
        
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def record_block(self, phase: Literal['imagination', 'perception'], image_name: str | None = None) -> dict:
        """
        Register a block of EEG data

        Args:
            duration (int): seconds to record
            phase (str): 'perception' or 'imagination'
            image_name (str | None): name of the image shown
        """
        
        start_ts = time.time()
        res = self.reader.raw_to_psd(seconds=2 if phase == 'perception' else 4)
        end_ts = time.time()
        print("Unknown PSD Data has been recorded")
        
        while res is None:
            print("Previous PSD Data was unclear, try again...")
            start_ts = time.time()
            res = self.reader.raw_to_psd(seconds=2 if phase == 'perception' else 4)
            end_ts = time.time()
            
        psd_data, channels_data = res
        print("Valid PSD Data has been recorded")
        
        self.image_name = image_name
            
        return {
            "timestamp_start": start_ts,
            "timestamp_end": end_ts,
            "phase": phase,
            "image_name": image_name,
            "raw": {ch: data.tolist() for ch, data in channels_data.items()},
            "psd": psd_data
        }
    
    def save(self, block: dict):
        """Save the recorded data to a JSON file
        """
        path = os.path.join(self.output_path, f"session_{block.get('timestamp_start', '')}_{os.path.basename(self.image_name).split('.')[0]}.json")
        with open(path, 'w') as f:
            json.dump(block, f, indent=4)
        print("Block has been saved")