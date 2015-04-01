import sys
import os
import json
import string

from productLoader import productsAsJson, categoryWords, descriptorWords
from categoryLoader import includeCategories
from wordsManipulator import *
#from splitTrainTest import initializeSplitDict, isTrain

def nlpTrainingLine_EN(desc_words, category_set, init_category_set):
    nlpdata_en = {}
    try:
        for w in desc_words:
            # for each word, make a decision
            # if w is part of the category inclusion set, keep it and make it a target word
            if w in init_category_set or w in category_set:
                nlpdata_en[w] = True
            else:
                nlpdata_en[w] = False
                    
        
        return nlpdata_en
    
    except Exception as e:
        print 'Exception: ', e
        return {}
    
## gennerate the training data for NLP 
def nlpTrainingData_EN(product_json, init_category_set, output_train_file, output_test_file, train_ids):
    total_words_train = 0
    total_words_test = 0
    total_pos_train = 0
    total_pos_test = 0
    train_prod_count = 0
    test_prod_count = 0
     
    output_train = open(output_train_file, 'w')
    output_test = open(output_test_file, 'w')
    
    #total_prod_count = len(product_json)
    #train_test_split = (0.8, 0.2)
    #splitDict = initializeSplitDict(total_prod_count, train_test_split)
    
    # loop over all the products in the list
    for i, d in enumerate(product_json):
        print 'Evaluating product ', d['id']
        # get category set
        cat_set = categoryWords(d['categories'])
        print 'Num category words ', len(cat_set)
        
        # split description by words
        desc_words = descriptorWords(d['description'])
        print 'Num desc words ', len(desc_words)
        # for each of the word, select if needs to be kept for NLP and if needed to be marked as Category
        nlpdata_en = nlpTrainingLine_EN(desc_words, cat_set, init_category_set)
        
        #if isTrain(splitDict):
        if i in train_ids:
            train_prod_count += 1
            total_words_train += len(nlpdata_en)
            
            # the training file should be word \t Category (or 0)            
            for w in nlpdata_en:
                # if a Category word or not
                if nlpdata_en[w]:
                    total_pos_train  += 1
                    output_train.write(w + "\t"+ "Category\n")
                else:
                    output_train.write(w + "\t"+ "0\n")
            if len(nlpdata_en):
                output_train.write("\n")
                
        else:
            test_prod_count += 1
            total_words_test += len(nlpdata_en)
            for w in nlpdata_en:
                # if a Category word or not
                if nlpdata_en[w]:
                    total_pos_test  += 1
                    output_test.write(w + "\t"+ "Category\n")
                else:
                    output_test.write(w + "\t"+ "0\n")
        
            #if len(nlpdata_en):
            #    output_test.write("\n")
    
    
    output_train.close()
    output_test.close()
    
    print 'Train: Total %d Pos %d '%(total_words_train, total_pos_train)
    print 'Test: Total %d Pos %d '%(total_words_test, total_pos_test)
    print 'Overall: Total %d Pos %d'%(total_words_train + total_words_test, total_pos_train + total_pos_test)
    
    print 'Ratio :Train/Total  Words : %f Pos: %f'%(float(total_words_train) /(total_words_train + total_words_test), 
                                                    float(total_pos_train) / (total_pos_train + total_pos_test))
    print 'Train products %d'%(train_prod_count)
    print 'Test products %d'%(test_prod_count)
    print 'Ratio products Train / Total %f'%(float(train_prod_count) / (train_prod_count + test_prod_count))
    
def usage():
    print __file__, 'product_json_file', 'initial category_json', 'output_train_file', 'output_test_file'
    sys.exit(1)


def main():
        
    if len(sys.argv) < 5:
        usage()
        
    product_json_filename = sys.argv[1]
    category_json_filename = sys.argv[2]
    output_train_filename = sys.argv[3]
    output_test_filename = sys.argv[4]
    train_id_file = sys.argv[5]
    
    f = open(train_id_file)
    train_ids = json.load(f)
    
    
    # load the product json file
    product_json = productsAsJson(product_json_filename)
    print 'Loaded product json file. Length = ', len(product_json)
    init_category_set = includeCategories(category_json_filename)
    print 'Loaded category set. Length = ', len(init_category_set)
    nlpTrainingData_EN(product_json, init_category_set, output_train_filename, output_test_filename, train_ids)
    
if __name__ == "__main__":
    main()
