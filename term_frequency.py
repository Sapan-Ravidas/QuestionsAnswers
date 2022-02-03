from enum import unique
from typing import Counter
from utils import Util

import nltk
import sys
import os
import string
import math


if __name__ == "__main__":
    dicrectory = "corpus"
    files = Util.load_files(dicrectory)

    file_words = { 
        filename : Util.tokenize(files[filename]) for filename in files 
    }

    tf = {}
    for filename, file_content in file_words.items():
        unique_words = Counter(file_content)
        N = len(file_content)
        
        

