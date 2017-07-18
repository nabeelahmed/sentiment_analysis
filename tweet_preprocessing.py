__author__ = 'nahmed'

import json
from nltk.tokenize import word_tokenize
import re


tokens_list = []  # for input sentiment analysis - train/fit some classifier
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

with open('data/stream_python.json', 'r') as f:
    # line = f.readline()  # read only the first tweet/line
    # tweet = json.loads(line)  # load it as Python dict
    # print(json.dumps(tweet, indent=4))  # pretty-print
    # print(word_tokenize(tweet))
    for line in f:
        tweet = json.loads(line)
        tokens = preprocess(tweet['text'])
        tokens_list.append(tokens)

print(tokens_list)
print(len(tokens_list))

