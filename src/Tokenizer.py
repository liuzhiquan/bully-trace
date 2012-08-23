#!/usr/bin/env python
# -*- coding: utf-8 -*-  


class Tokenizer():
    """Turn a string into a list of tokens"""
    
    def __init__(self):
        self.toLower = True
        self.anonymous = True
        self.emoticons = True
        self.removeRT = True
        self.removeURL = True
    
    def tokenize(self, text):
        """Turn a string into a list of tokens"""
        if self.removeRT:
            if text.startswith('RT'):
                return []
        if self.toLower:
            text = text.lower()
        tokens = text.split()
        
        if self.anonymous:
            '''
            newTokens = []
            for token in tokens:
                if token.startswith('@'):
                    token = '@USER'
                newTokens.append(token)
            tokens = newTokens
            '''
            tokens = [token if not token.startswith('@') else '@USER' for token in tokens ]
        if self.removeURL:
            tokens = [token if not token.startswith('http://') else 'HTTPLINK' for token in tokens]
        
        return tokens

def main():
    T = Tokenizer()
    for line in open('tweets.txt').readlines()[200:300]:
        print line
        print ' '.join(T.tokenize(line))
        print

if __name__ == '__main__':
    main()     
