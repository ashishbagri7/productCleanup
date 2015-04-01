
import random
import math 

def initializeSplitDict(total_samples, split_ratio = (0.8, 0.2)):
    # initialize the split dict
    # takes in the ratio of the split required 
    # split ratio should be a tuple with train and test values
    if len(split_ratio) != 2 and sum(split_ratio) != 1.0:
        raise Exception("Split ratio must be a tuple of length 2 and must sum to 1")
    
    random.seed()
    random_state = random.getstate()
    
    splitDict = {}
    
    splitDict['split_ratio'] = split_ratio
    splitDict['random_state'] = random_state
    splitDict['total_samples'] = total_samples
    splitDict['train_samples'] = math.floor(total_samples*split_ratio[0])
    splitDict['test_samples'] = total_samples - splitDict['train_samples'] 
    
    return splitDict
     

def isTrain(splitDict):
    
    random.setstate(splitDict['random_state'])
    
    thresh = splitDict['train_samples']  / (splitDict['train_samples'] + splitDict['test_samples'])
    
    x = random.random()
    splitDict['random_state'] = random.getstate()
    train = False
    
    if x > thresh:
        # make it test
        splitDict['test_samples'] = splitDict['test_samples'] - 1
    else:        
         splitDict['train_samples'] = splitDict['train_samples'] - 1
         train = True
    
    return train 
        
    

def test():
    a = range(1, 10)
    splitDict = initializeSplitDict(len(a))
    for i in a:
        print i, isTrain(splitDict)
    
    
    print splitDict

    