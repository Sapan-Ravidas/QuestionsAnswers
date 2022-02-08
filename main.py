from gettext import find
from itertools import count
from socket import NI_DGRAM
from sre_constants import BRANCH
from utils import Util
import utils

import sys
import nltk

# nltk.download("wordnet")
# nltk.download('omw-1.4')
# nltk.download("stopwords")

FILE_MATCHES = 5
SENTENCE_MATCHES = 1

DIFF = set([10, 14, 33, 37, 48, 53, 55, 56, 60, 64, 65, 69, 72, 73, 74, 78, 80, 83])


def find_matches(query, file_words, file_idfs):
    # Determine top file matches according to TF-IDF
    try:
        filenames = util.top_files(query, file_words, file_idfs, n=FILE_MATCHES) 

        # Extract Sentences from top files
        sentences = dict()
        for filename in filenames:
            for passage in files[filename].split("\n"):
                for sentence in nltk.sent_tokenize(passage):
                    tokens = Util.tokenize(sentence)
                    if tokens:
                        sentences[sentence] = tokens
    
        # Compute IDF-values accross sentences
        idfs = Util.compute_idfs(sentences)

        # Determine top sentence matches
        matches = util.top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
        if not matches:
            return {'Couldn\'t find the answer'}
        return matches
    except:
        return {'Couldn\'t find the answer...'}



def print_matches(matches):
    """
    Print all the matching sentences for query
    """
    for match in matches:
        print(match, end=",")


def writeToFile(query, ans_file, counter, matches):
    """
    Write the matching sentences in a file for output
    """
    ans_file.writelines(f"{counter}. {query}")
    for match in matches:
        ans_file.writelines(match)
    
    ans_file.writelines("\n")
    ans_file.writelines("\n")



if __name__ == '__main__':
    # check command-line arguments
    util = Util()
    N_ARGS = len(sys.argv)
    
    if N_ARGS not in  {2, 3}:
        sys.exit("Usage: python main.py corpus")

    # Mapping of filename : content
    files = Util.load_files(sys.argv[1])

    file_words = {
        filename : Util.tokenize(files[filename]) for filename in files
    }

    # Calculate the IDF values accrosss the files
    file_idfs = Util.compute_idfs(file_words)
    
    if N_ARGS == 2:
        CHOICE = "Y"
        while CHOICE.lower() in {'y', 'yes'}:
            # Prompt user for query
            query = set(Util.tokenize(input("Query: ")))
            matches = find_matches(query, file_words, file_idfs)

            print_matches(matches)
            print("------>")
            CHOICE = input("Want to continue? yes/no : ")
    
    elif N_ARGS == 3:
        q_file = sys.argv[2]
        with open(q_file) as questions:
            counter = 1
            while True:
                Q = questions.readline()
                if Q == "" or Q == None: break
                if counter in DIFF:
                    print(Q.strip("\n"), end="\t")
                    matches = find_matches(set(Util.tokenize(Q)), file_words, file_idfs)
                    # writeToFile(Q, answers, counter, matches)
                    # print_matches(matches)
                counter += 1
                    