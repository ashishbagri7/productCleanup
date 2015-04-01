

import enchant
import string

# yang : 'which' , 'para' : 'the'
ignore_words = {'yang', 'para'}
englishDict = enchant.Dict("en_US")
exclude_punctuation = set(string.punctuation)

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


def isEnglish(word):
    global englishDict
    try:
        return englishDict.check(word)
    except Exception as e:
        print e
        return False
    
def cleanPuntuation(word):
    w = ''.join(ch for ch in word if ch not in exclude_punctuation)
    return w
