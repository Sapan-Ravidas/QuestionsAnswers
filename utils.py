from socket import socket
import nltk
import sys
import os
import string
import math

class Util:

    @classmethod
    def load_files(cls, directory):
        """
        Given a directory name, return a dictionary mapping the filename of each file
        `.txt` file inside that directory to the file's contents as a string 
        """
        dictionry = {}
    
        for file in os.listdir(directory):
            with open(os.path.join(directory, file), encoding="utf-8") as ofile:
                dictionry[file] = ofile.read()
    
        return dictionry


    @classmethod
    def tokenize(cls, document):
        """
        Given a document (represented as a string), return a list of all of the
        words in that document, in order.

        Process document by coverting all words to lowercase, and removing any
        punctuation or English stopwords.
        """
        tokenized = nltk.tokenize.word_tokenize(document.lower())
        final_list = [x for x in tokenized if x not in string.punctuation and x not in nltk.corpus.stopwords.words("english")]
        return final_list



    @classmethod
    def compute_idfs(cls, documents):
        """
        Given a dictonary of 'documents' that maps names of documents to a list
        of words, return a dictionary that maps words to their IDF values

        Any word that appears in at-least one of the documents  should be in the
        resultig dictionary.
        """
        idf_dictio = {}
        doc_len = len(documents)

        unique_words = set(sum(documents.values(), []))
    
        for word in unique_words:
            count = 0
            for doc in documents.values():
                if word in doc:
                    count += 1
        
            idf_dictio[word] = math.log(doc_len / count)
    
        return idf_dictio



    def show_FileRelevance(self, scores):
        """
        Given the 'scores' (a dictionary mapping filename to relevance score)
        Displays relevance score for all the files
        """
        try:
            for key, value in sorted(scores.items(), key = lambda x : x[1], reverse=True):
                print(key, end="\t")
                print(value, end="\t")
                break
        except Exception as e:
            print(e)


    
    def show_SentenceRelevance(self, scores):
        """
        Given the scores (a dictionaty mapping the senetences to their respected scores
        and density). Displays the scores of top 5 sentence.
        """
        try:
            for key, value in sorted(scores.items(), key = lambda x: (x[1][0], x[1][1]), reverse=True):
                print(key, end="\t")
                print(value[0], end="\n")
                break
        except Exception as e:
            print(e)



    def top_files(self, query, file_words, idfs, n):
        """
        Given a 'query' (a set of words), 'files_words' (a dictinary mapping names
        of files to a list of their words), and 'idfs' (a dictionary mapping words
        to their IDF value), returns a list of the filenames of the 'n' top files 
        that matches the query, ranked according to tf-idf
        """

        scores = {}
        for filename, file_content in file_words.items():
            file_score = 0
            for word in query:
                if word in file_content:
                    file_score += file_content.count(word) * idfs[word]
                    # file_score += ((file_content.count(word) / len(file_content)) * idfs[word])

            if file_score != 0:
                scores[filename] = file_score
        self.show_FileRelevance(scores)
        sorted_by_score = [k for k, v in sorted(scores.items(), key=lambda x : x[1], reverse=True)]
        return sorted_by_score[:n]



    def top_sentences(self, query, sentences, idfs, n):
        """
        Given a 'query (a set of words), 'sentences' (a dictionary mapping sentecnes
        to a list of their words), nd 'idfs' (a dictionary mapping words to their IDF
        values), return a list of the 'n'n top sentences that match the query, ranked
        according to IDF. If there are ties, preference should be given to sentence 
        that have a hiher query density. 
        """
        scores = {}
        for sentence, sentwords in sentences.items():
            score = 0
            for word in query:
                if word in sentwords:
                    score += idfs[word]
        
            if score != 0:
                density = sum([sentwords.count(x) for x in query]) / len(sentwords)
                scores[sentence] = (score, density)
    
        self.show_SentenceRelevance(scores) # Show top sentences by the relevance-scores 

        sorted_by_score = [k for k, v in sorted(scores.items(), key = lambda x : (x[1][0], x[1][1]), reverse=True)]
        return sorted_by_score[:n]
