

'''
Builds the autocomletion list 
Adds the brands into the existing list

'''

import os
import sys
import time

sys.path.insert(0, '../')

from brandsLoader import updateBrand
from categoryCalculator import updateTags
from categoryLoader import loadCategories
from productLoader import productsAsJson
from utils import sort_dict
from wordsManipulator import ignorePunctuations, asciiLower, stripPunctuations

def addBrandsToTagDict(brands, tag_dict, skip_count):
    if skip_count:
        for b in brands:
            tag_dict[b] = None
    else:
        for b in brands:        
            if b in tag_dict:
                tag_dict[b] += brands[b]
            else:
                tag_dict[b] = brands[b]
    
    return tag_dict

def autoCompleteTags(category_db, brands, skip_counts):
    tag_dict = {}
    
    for cid in category_db:
        category = category_db[cid]
        en = stripPunctuations(category['catname_en']).replace("-", " ")
        if skip_counts:
            tag_dict[en] = None
        else:            
            if en in tag_dict:
                tag_dict[en] = max(tag_dict[en], category['cat_count'])
            else:
                tag_dict[en] = category['cat_count']
        
        ind = stripPunctuations(category['catname_ind']).replace("-", " ")
        if skip_counts:
            tag_dict[ind] = None
        else:
            if ind in tag_dict:
                tag_dict[ind] = max(tag_dict[ind], category['cat_count'])
            else:
                tag_dict[ind] = category['cat_count']
                
        
        for ele in category['catset_en']:
            tag_ele = stripPunctuations(ele).replace("-", " ")
            if skip_counts:
                tag_dict[tag_ele] = None
            else:
                if tag_ele in tag_dict:
                    tag_dict[tag_ele] = max(tag_dict[tag_ele], category['catset_en_count'][ele])
                else:
                    tag_dict[tag_ele] = category['catset_en_count'][ele]
        
        for ele in category['catset_ind']:
            tag_ele = stripPunctuations(ele).replace("-", " ")
            if skip_counts:
                tag_dict[tag_ele] = None
            else:
                if tag_ele in tag_dict:
                    tag_dict[tag_ele] = max(tag_dict[tag_ele], category['catset_ind_count'][ele])
                else:
                    tag_dict[tag_ele] = category['catset_ind_count'][ele]
    
        
    
    tag_dict = addBrandsToTagDict(brands, tag_dict, skip_counts)
    
    if not skip_counts:
        tag_dict_sorted = sort_dict(tag_dict, reverse=True)
        return tag_dict_sorted
    else:
        return tag_dict

def includeTag(tagname):
    if tagname == 'unknown' or len(tagname) < 2:
        return False
    else:
        return True
    
def printhelp():
    if len(sys.argv) < 4:
        print __file__, 'tags_json', 'products_json', 'output_file', 'skip_counts = True'
        sys.exit(1)
        
def main():
    printhelp()
    
    tags_file = sys.argv[1]
    products_file = sys.argv[2]
    output_file = sys.argv[3]
    
    
    skip_counts = True
    if len(sys.argv) > 4:
        if sys.argv[4].lower() == 'false':
            skip_counts = False
    
    tags_db = loadCategories(tags_file, True)
    #print 'Number of category tags: ', len(tags_db)
    
    products = productsAsJson(products_file)
    total_products = len(products)
    #print 'Number of products : ',total_products 
    
    #print 'The output file is ', output_file
    
    brands = {'unknown': 0}
    
    for i, product in enumerate(products):
        if not skip_counts:
            updateTags(i, product, tags_db)
        
        updateBrand(product, brands)
            
    tag_dict_sorted = autoCompleteTags(tags_db, brands, skip_counts)    
    tag_autocomplete = open(output_file, 'w')
    
    #print 'Write autocomplete tags to file ', output_file
    
    if skip_counts:
        for ele in tag_dict_sorted:
            if includeTag(ele):
                tag_autocomplete.write(ele)
                tag_autocomplete.write("\n")
    else:
        for ele in tag_dict_sorted:
            if includeTag(ele[0]):
                tag_autocomplete.write(','.join([ele[0], str(ele[1])]))
                tag_autocomplete.write("\n")
                
    tag_autocomplete.close()
    #print 'Completed writing autocomplete tags'
    
main()      