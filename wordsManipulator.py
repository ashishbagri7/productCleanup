

import enchant
import re
import string


# yang : 'which' , 'para' : 'the'
ignore_words = {'yang', 'para'}

englishDict = enchant.Dict("en_US")

def ignoreWord(word):
    if word in ignore_words:
        return True
    
    return False

def englishWords(words, englishDict, exclude):
    engwords = []
    try:
        for w in words:
            w = w.encode('ascii', 'ignore').lower()
            w = ''.join(ch for ch in w if ch not in exclude)
            # len(w) > 1 as dont need single words like x        
            if len(w) > 1 and englishDict.check(w) and not ignoreWord(w):
                engwords.append(w)
                
    except Exception as e:
        print 'Exception: ', e
        print 'Words = ', words
                
    return engwords


def asciiLower(mystring):
    return mystring.encode('ascii', 'ignore').rstrip().lower()

def isEnglish(word):
    global englishDict
    try:
        return englishDict.check(word)
    except Exception as e:
        print e
        return False
    

def stripPunctuations(word):
    return word.rstrip('\'\"-,.:;!?\n ')    
    
'''
Ignore punctuations from a word/line and return 
the cleaned out word
This ignore spaces in between !
'''
def ignorePunctuations(word):
    x = re.split('\W+', word)
    x = filter(None, x)
    return ''.join(x)
 
'''
Takes in an entity and returns the set of words per line of this entity

take an entity: could be description, title, catgories
 makes it into a list of list with all the individual words
 stripped out of all punctuations
'''
def entity2words(entity):
    # convert to ascii and lower it
    entity = asciiLower(entity)
    # split it to individual lines
    lines = entity.split("\n")
    return_list = []
    # for each line, there must be a list
    for line in lines:
        x = re.split('\W+', line)
        x = filter(None, x)
        if len(x):
            return_list.append(x)

    # list of list
    return return_list
