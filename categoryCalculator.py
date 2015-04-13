
'''
Take in a product json and return the tags found for this product.
The tags are form of dict and are weighted and orderd
**** Must update counts here as this takes in a product and returns the tags ****
'''

import json
import logging
import sys

from categoryLoader import categoryItems
from wordsManipulator import entity2words, ignorePunctuations, asciiLower

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

def updateTags(pid, product_json, category_db):   
    category_found, subtags_found = categorizeProduct(product_json, category_db)
    logging.info('%s) Pid: %s : %s' % (str(pid), product_json['id'], json.dumps(category_found)))
        
    # Increment subtags_found_count for all subtags that have been found
    for cid in subtags_found:
        if len(subtags_found[cid]['en']):
            for ele in subtags_found[cid]['en']:
                category_db[cid]['catset_en_count'][ele] += 1
        
        if len(subtags_found[cid]['ind']):
            for ele in subtags_found[cid]['ind']:
                category_db[cid]['catset_ind_count'][ele] += 1
        
        if (len(subtags_found[cid]['en']) + len(subtags_found[cid]['ind'])) > 0:
            category_db[cid]['cat_count'] += 1
        

def foo(subtags_dict_n, subtags_found):
    
    for k in subtags_dict_n:
        if k not in subtags_found:
            subtags_found[k] =  {'en': set(), 'ind': set()}
                        
        subtags_found[k]['en'] = subtags_found[k]['en'].union(subtags_dict_n[k]['en'])
        subtags_found[k]['ind'] = subtags_found[k]['ind'].union(subtags_dict_n[k]['ind'])
    
        
'''
Take in a product json and return the tags found for this product.
The tags are form of dict and are weighted and orderd
**** Must update counts here as this takes in a product and returns the tags ****
'''
def categorizeProduct(product_json, category_db):
    
    category_found = {'description': [], 'title': [], 'categories': []}
    # key ==> cat_id. value => en, ind sets 
    subtags_found = {}
    
    if 'description' in product_json:
        descr_list = entity2words(product_json['description'])
        category_list, subtags_dict_1 = entity2category(descr_list, category_db)
        foo(subtags_dict_1, subtags_found)
        category_found['description'].extend(category_list)
            
    
    if 'title' in product_json:
        title_list = entity2words(product_json['title'])
        category_list, subtags_dict_2 = entity2category(title_list, category_db)
        foo(subtags_dict_2, subtags_found)
        category_found['title'].extend(category_list)
        
    if 'categories' in product_json:
        # deal with categories differently due to its structure
        clist = categoryItems(product_json['categories'])
        for l in clist:
            category_list , subtags_dict_3 = entity2category(l, category_db)
            foo(subtags_dict_3, subtags_found)
            category_found['categories'].extend(category_list)
    
    return category_found, subtags_found
    
'''
Takes in a entity and returns the categories found in this entity

'''
def entity2category(entity_list, category_db):
    # entity_list is a list of list
    category_found = []
    subtags_found = {}
    
    for line in entity_list:
        cf = getCommonCategory(line, subtags_found, category_db)
        if len(cf):
            category_found.extend(cf)
            cdebug = [(category_db[cid]['catname_en'], category_db[cid]['catname_ind']) for cid in cf]
            #logging.debug("%s --> %s" % (json.dumps(line), json.dumps(cdebug)))

    return category_found, subtags_found

'''
Takes in word_list which is the words from any given line 
Returns the categories found in this line
'''
def getCommonCategory(word_list, subtags_found, category_db):
    category_found = []
    
    # get the categories from these word set
    # for all categories in the database
    for cat_id in category_db:
        if compareCategory(word_list, category_db[cat_id], subtags_found):
            category_found.append(cat_id)
        
    return category_found



'''
TDOO: Update this method to make a comparision even when there is not an exact match
word_list = words part of a line
catname = name of the category

Takes in words from a line and a given category and finds if there is a match with this
category
'''

def compareCategoryItem(word_list, catname):
    # split catname by "-".
    # can be certain that the names do not have spaces or other punctuations
    catnameparts = catname.split("-")
    if set(catnameparts).issubset(set(word_list)):
        return True
    else:
        return False   


# word list is a line of the data. 
# since there are multiple lines in the product,
# cannot increase counts here of cat found
def compareCategory(word_list, category, subtags_found):
    cat_match = False
    
    # for each element in catset_en
    for ele in category['catset_en']:
        if compareCategoryItem(word_list, ele):
            # found the category with sub tag : ele
            if category['cat_id'] not in subtags_found:
                subtags_found[category['cat_id']] =  {'en': set(), 'ind': set()}
            
            subtags_found[category['cat_id']]['en'].add(ele)
            
            cat_match = True
    
    for ele in category['catset_ind']:
        if compareCategoryItem(word_list, ele):
            # found the category
            if category['cat_id'] not in subtags_found:
                subtags_found[category['cat_id']] =  {'en': set(), 'ind': set()}
            
            subtags_found[category['cat_id']]['ind'].add(ele)
            
            cat_match = True
    
    return cat_match
