'''
creating N(N=2) word cloud from the 
title to find out interesting words
can extend to other fields like description or categories.name if needed
'''

import sys

from productLoader import productsAsJson
from utils import sort_dict
from wordsManipulator import entity2words, ignorePunctuations, asciiLower


def print_help():
    
    if len(sys.argv) < 3:
        print __file__, 'product_json_file', 'N_word_cloud'
        sys.exit(1)

def ele_len(ele):
    return len(ele) > 1

def buildWordCloud(product,key,N, wordcloud):
    word_list = entity2words(product[key])
    for line in word_list:
        for i, word in enumerate(line):
            w = line[i:min(len(line), i+N)]
            w = filter(ele_len, w)
            if len(w) == N:
                x = ' '.join(w)
                if x not in wordcloud:
                    wordcloud[x] = 1
                else:
                   wordcloud[x] += 1                                 
        
def main():
    print_help()
    product_filename = sys.argv[1]
    N = int(sys.argv[2])
    
    products = productsAsJson(product_filename)
        
    wordcloud = {}
    for product in products:
        buildWordCloud(product,'title', N, wordcloud)
    
    wordcloud_sorted = sort_dict(wordcloud, reverse=True)
    for w in wordcloud_sorted:
        print w
    
    
main()
    