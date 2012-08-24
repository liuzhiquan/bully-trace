#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import getopt
import os
import math
import re
import string
import random

import MySQLdb as db

class NaiveBayes:
    class TrainSplit:
        """Represents a set of training/testing data. self.train is a list of Examples, as is self.test. 
        """
        def __init__(self):
            self.train = []
            self.test = []

    class Example:
        """Represents a document with a label. klass is 'pos' or 'neg' by convention.
             words is a list of strings.
        """
        def __init__(self):
            self.klass = ''
            self.words = []
            self.content = ''


    def __init__(self):
        """NaiveBayes initialization"""
        self.FILTER_STOP_WORDS = False
        self.stopList = set([line.strip() for line in open('english.stop', 'r').readlines()])
        self.numFolds = 10
        
        self.posDict = {}
        self.negDict = {}
        self.posExampleNum = 0
        self.negExampleNum = 0
        self.posTokenNum = 0
        self.negTokenNum = 0

        self.priorPosScore = 0.0
        self.priorNegScore = 0.0
        ####
        self.wordScores = {}
    
    
    def classify(self, words):
        """
            'words' is a list of words to classify. Return 'pos' or 'neg' classification.
        """
        
        posScore = math.log(1.0 * self.posExampleNum / (self.posExampleNum + self.negExampleNum))
        negScore = math.log(1.0 * self.negExampleNum / (self.posExampleNum + self.negExampleNum))
        posTermNum = len(self.posDict)
        negTermNum = len(self.negDict)
        
        for word in words:
            posScore += math.log(1.0 * (self.posDict.get(word, 0) + 1) / (self.posTokenNum + posTermNum))
            negScore += math.log(1.0 * (self.negDict.get(word, 0) + 1) / (self.negTokenNum + negTermNum))

        if posScore > negScore: return 'pos'
        else: return 'neg'
    
    def train(self, trainData):
        
        for example in trainData:
            words = example.words
            if self.FILTER_STOP_WORDS:
                words = self.filterStopWords(words)
            self.addExample(example.klass, words)
        
        self.priorPosScore = math.log(1.0 * self.posExampleNum / (self.posExampleNum + self.negExampleNum))
        self.priorNegScore = math.log(1.0 * self.negExampleNum / (self.posExampleNum + self.negExampleNum))

        posTermNum = len(self.posDict)
        negTermNum = len(self.negDict)

        posScore = 0.0
        negScore = 0.0
        for word in self.posDict.keys() + self.negDict.keys():
            posScore += math.log(1.0 * (self.posDict.get(word, 0) + 1) / (self.posTokenNum + posTermNum))
            negScore += math.log(1.0 * (self.negDict.get(word, 0) + 1) / (self.negTokenNum + negTermNum))
        
            self.wordScores[word] = {}
            self.wordScores[word]['posScore'] = posScore
            self.wordScores[word]['negScore'] = negScore

    
    def addExample(self, klass, words):
        """
         * Train your model on an example document with label klass ('pos' or 'neg') and
         * words, a list of strings.
         * Returns nothing
        """
        if klass == 'pos':
            self.posExampleNum += 1
            for word in words:
                self.posDict[word] = self.posDict.get(word, 0) + 1
                self.posTokenNum += 1
        elif klass == 'neg': 
            self.negExampleNum += 1
            for word in words:
                self.negDict[word] = self.negDict.get(word, 0) + 1
                self.negTokenNum += 1
    
    
    def segmentWords(self, text):
        """
         * Splits lines on whitespace for file reading
        """
        text = text.lower()

        # reserve these symbols:  : ( )
        # remove the punctuation gives better accuracy
        pattern = re.sub(r'[:()]', '', string.punctuation)
        text = re.sub(r'[%s]' % pattern, '', text)
        
        return text.split()

    
    def buildSplits(self):
            ################
        """Builds the splits for training/testing"""

        #databases: OpinionMiningOnTwitter
        #tables: gold_standard_movie
        #        gold_standard_person
        #        twitterdata_movie
        #        twitterdata_person
        # gold_standard_movie format: (id, topic, content, polarity, sentiment_expression)
        #example:('9798541400', 'Shutter Island', "I lied to my girl and told her I haven't seen Shutter Island yet, Now I'll be going to see it for the 2nd time in 1 day!!", 'void', '')
        # polarity: 'pos' or 'neg' or 'neu' or 'void'
        # twitterdata_movie 
        #format: (id, content, topic)

        con = db.connect(host='localhost', user='root', passwd='', db='OpinionMiningOnTwitter')


        cur = con.cursor(db.cursors.DictCursor)
        cur.execute('SELECT * from gold_standard_person')
        rows = cur.fetchall()
        cur.close()
        con.close()


        examples = []
        for row in rows:
            example = self.Example()
            example.klass = row['polarity']
            example.content = row['content']
            example.words = self.segmentWords(example.content)
            if example.klass == 'pos' or example.klass == 'neg':
                examples.append(example)
        

        splits = []
        foldSize = int(1.0 * len(examples) / self.numFolds)
        
        random.shuffle(examples)

        for i in range(self.numFolds):
            split = self.TrainSplit()
            split.test = examples[i*foldSize :i*foldSize+foldSize]
            split.train = examples[:i*foldSize] + examples[i*foldSize+foldSize:]
            splits.append(split)
        return splits
    

    def filterStopWords(self, words):
        """Filters stop words."""
        filtered = []
        for word in words:
            if not word in self.stopList and word.strip() != '':
                filtered.append(word)
        return filtered



def main():
    nb = NaiveBayes()
    (options, args) = getopt.getopt(sys.argv[1:], 'f')
    if ('-f','') in options:
        FILTER_STOP_WORDS = True
    else:
        FILTER_STOP_WORDS = False
    
    splits = nb.buildSplits()
    avgAccuracy = 0.0
    fold = 0
    for split in splits:
        classifier = NaiveBayes()
        classifier.FILTER_STOP_WORDS = FILTER_STOP_WORDS

        accuracy = 0.0

        classifier.train(split.train)
        ''' 
        for example in split.train:
            words = example.words
            if classifier.FILTER_STOP_WORDS:
                words = classifier.filterStopWords(words)
            classifier.addExample(example.klass, words)
        '''

        f = open('debug', 'w')
        for example in split.test:
            words = example.words
            if classifier.FILTER_STOP_WORDS:
                words = classifier.filterStopWords(words)
            guess = classifier.classify(words)
            if example.klass == guess:
                accuracy += 1.0
            
            print >> f, 'gold standard: %s\tclassifier: %s\ntweet content: %s' \
                         % (example.klass, guess, example.content)
    
            print >> f, 'word scores: %s\n' % '\n'.join(['%s:\tpos:%f\tneg:%f' \
                % (word, classifier.wordScores[word]['posScore'], classifier.wordScores[word]['negScore']) \
                for word in example.words if word in classifier.wordScores])
            print >> f
            print >> f

        f.close()

        f = open('word_scores', 'w')
        for word in classifier.wordScores:
            posScore = classifier.wordScores[word]['posScore']
            negScore = classifier.wordScores[word]['negScore']

            f.write('word: %s' % word)
            if posScore == negScore:
                f.write('\tpos=neg')
            elif posScore > negScore:
                f.write('\tPOS')
            else:
                f.write('\tNEG')
            f.write('\tposScore: %f\tnegScore: %f' % (posScore, negScore))
            f.write('\n')
        f.close()


        accuracy = accuracy / len(split.test)
        avgAccuracy += accuracy
        print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy) 
        fold += 1
    avgAccuracy = avgAccuracy / fold
    print '[INFO]\tAccuracy: %f' % avgAccuracy

if __name__ == "__main__":
    main()
