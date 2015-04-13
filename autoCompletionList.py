
import operator
import sys
import time

from categoryCalculator import updateTags
from categoryLoader import loadCategories
from productLoader import productsAsJson
from wordsManipulator import ignorePunctuations, asciiLower


def addBrandsToTagDict(brands, tag_dict):
    for b in brands:
        if b in tag_dict:
            tag_dict[b] += brands[b]
        else:
            tag_dict[b] = brands[b]
    
    return tag_dict

def autoCompleteTags(category_db, brands):
    tag_dict = {}
    
    for cid in category_db:
        category = category_db[cid]
        
        if category['catname_en'] in tag_dict:
            tag_dict[category['catname_en']] = max(tag_dict[category['catname_en']], category['cat_count'])
        else:
            tag_dict[category['catname_en']] = category['cat_count']
        
        if category['catname_ind'] in tag_dict:
            tag_dict[category['catname_ind']] = max(tag_dict[category['catname_ind']], category['cat_count'])
        else:
            tag_dict[category['catname_ind']] = category['cat_count']
        
        for ele in category['catset_en']:
            if ele in tag_dict:
                tag_dict[ele] = max(tag_dict[ele], category['catset_en_count'][ele])
            else:
                tag_dict[ele] = category['catset_en_count'][ele]
        
        for ele in category['catset_ind']:
            if ele in tag_dict:
                tag_dict[ele] = max(tag_dict[ele], category['catset_ind_count'][ele])
            else:
                tag_dict[ele] = category['catset_ind_count'][ele]
    
    
    tag_dict = addBrandsToTagDict(brands, tag_dict)
    
    tag_dict_sorted  = sorted(tag_dict.items(), key=operator.itemgetter(1), reverse=True)
    return tag_dict_sorted

def updateBrand(p, brands):
    if 'brand' in p:
        b = ignorePunctuations(asciiLower(p['brand']))
        if len(b) > 0:
            if b in brands:
                brands[b] += 1
            else:
                brands[b] = 1
        else:
            brands['unknown'] += 1
        
    else:
        brands['unknown'] += 1


def main():
    if len(sys.argv) < 4:
        printhelp()
        
    category_file = sys.argv[1]
    products_file = sys.argv[2]
    output_file = sys.argv[3]
    
    category_db = loadCategories(category_file, True)
    print 'Number of category tags: ', len(category_db)
    
    products = productsAsJson(products_file)
    total_products = len(products)
    print 'Number of products : ',total_products 
    
    print 'The output file is ', output_file
    
    brands = {'unknown': 0}
        
    for i, product in enumerate(products):
        if i and i % 100 == 0:
            print 'Completed ', i, 'out of ', total_products
        updateTags(i, product, category_db)
        updateBrand(product, brands)
                            
    tag_dict_sorted = autoCompleteTags(category_db, brands)
    tag_autocomplete = open(output_file, 'w')
    
    print 'Write autocomplete tags to file ', output_file
    
    for ele in tag_dict_sorted:
        tag_autocomplete.write(','.join([ele[0], str(ele[1])]))
        tag_autocomplete.write("\n")
    
    tag_autocomplete.close()
    print 'Completed writing autocomplete tags'
    
main()      