import pandas as pd
import glob
import os
import sys
import re
import csv

path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, "bloomberg_news")

print(path)
from os import walk

#b, a, all_files = next(walk(path))

all_folders = glob.glob(os.path.join(path, "*"))
AMOUNT = 500
all_folders = all_folders[-500:]
all_files = []
[all_files.extend(glob.glob(os.path.join(f, "*"))) for f in all_folders]

print("total files found: ", len(all_files))

def get_matching_line(text, pattern):
    lines = text.split("\n")
    for line_i in range(len(lines)):
        if(pattern in lines[line_i]):
            return line_i
    return 9999

def strip_start(text):
    pattern = "www.bloomberg.com"
    i = get_matching_line(text, pattern)
    text = text.split("\n", i+1)
    if(i < 9998):
        #print(text)
        return text[i+1]
    else:
        return ""

def strip_end(text):
    text = text.split("To contact the reporter")[0]
    text = text.strip()
    return text
cols = ["date", "filename", "text"]
rows = []
for _file in all_files[:]:
    filename = os.path.basename(_file)
    dirname = os.path.dirname(_file)
    dirname = dirname.split("/")[-1]
    with open(_file,'r') as f:
        text = f.read()

        text = strip_start(text)
        if(text == ""):
            continue
        text = strip_end(text)
        if(text == ""):
            continue
        #print(text)
        rows.append([dirname, filename, text])
df = pd.DataFrame(rows, columns = cols)

#print(df.text[3])
print(df.shape)

df.to_csv('bloomberg_out.zip', index=False, compression="zip")

sys.exit()