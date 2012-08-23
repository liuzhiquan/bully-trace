#!/usr/bin/env python
# -*- coding: utf-8 -*-  


class TweetFilter():
    """Filter the tweets crawled by Twitter API"""
    
    def __init__(self):
        pass
    
    def filter1(self, tweet):
        """filter raw tweets crawled from Twitter API,
        remove retweets (start with RT) and those which do not include 'bully', 
        so that we can label the tweets"""
        
        elems = tweet.split('\t')
        if len(elems) >= 2:
            tweetText = elems[1]
        else:
            return '' 
        if tweetText.startswith('RT'):
            return ''
        lowerTweet = tweetText.lower()
        if lowerTweet.find('bull') < 0:
            return ''
        return tweet
    
    def filter2(self, lines):
        """filter the labeled tweets.
        return a list of pairs (tweet, label)
        This fucntion will be removed later"""
        results = []
        for line in lines:
            elems = line.strip().split('\t')
            if len(elems) == 3:
                tweet_text = elems[1]
                if elems[2] == 'yes':
                    results.append((tweet_text, 1))
                elif elems[2] == 'no':
                    results.append((tweet_text, 0))
        
        return results
            
        
    
def filter1():
    Filter = TweetFilter()
    tweets = []
    for line in open('labeledTweets.txt').readlines():
        if Filter.filter1(line):
            tweets.append(line)
    f = open('labeledTweets2', 'w')
    print >> f, ''.join(tweets)
    f.close()
    
def filter2():
    Filter = TweetFilter()
    
    lines = Filter.filter2(open('labeledTweets2').readlines())
    f1 = open('1.txt', 'w')
    f0 = open('0.txt', 'w')
    for tweet_text, label in lines:
        if label == 1:
            print >> f1, tweet_text
        else:
            print >> f0, tweet_text
    
    
if __name__ == '__main__':
    filter2()
          