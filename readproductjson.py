import sys
import os
import json
import enchant
import string

            
def alternateProductCat(json_data_list):
    englishCatFill = []
    englishCatEmpty = []
    englishDict = enchant.Dict("en_US")
    exclude = set(string.punctuation)
    exclude.add("\n")
    exclude.add(" ")
    # loop over all the products in the list
    for i, d in enumerate(json_data_list[0:25]):
        prod_dict = {}
        had_orig_cat = False
        prod_dict['id'] =  d['id']
        words = d['description'].rstrip().split(" ")
        prod_dict['description'] = englishWords(words, englishDict, exclude)
        titlewords = d['title'].rstrip().split(" ")
        prod_dict['title'] = englishWords(titlewords, englishDict, exclude)
        prod_dict['categories'] = []
        original_cat = []
        # all existing categories  
        for c in d['categories']:
            if 'name' in c:
                had_orig_cat = True
                original_cat.append(c['name'].encode('ascii', 'ignore').rstrip().lower())
                cnamelist = c['name'].encode('ascii', 'ignore').rstrip().split(" ")
                cnamelist_en = englishWords(cnamelist, englishDict, exclude)
                if len(cnamelist_en) > 0:
                    prod_dict['categories'].append(' '.join(cnamelist_en))
        
        prod_dict['original_cat'] = original_cat
        
        if len(prod_dict['categories']) > 0:
            englishCatFill.append(prod_dict)
        else:
            prod_dict['had_orig_cat'] = had_orig_cat
            englishCatEmpty.append(prod_dict)
    
    print 'Filled : '
    for f in englishCatFill:
        print f
    
    print 'Empty : '
    for f in englishCatEmpty:
        print f
    print 'num of filled : ', len(englishCatFill)
    print 'num of empty : ', len(englishCatEmpty)
        
def categoryInfo(json_data):
    no_cat_key = []
    no_cat_value = []
    categories = {}
    for i, d in enumerate(json_data):
        if 'categories' not in d:
            no_cat_key.append(i)
            continue
        if len(d['categories']) == 0:
            no_cat_value.append(i)
            continue
        for c in d['categories']:
            if 'name' in c:
                n = c['name'].encode('ascii', 'ignore').lower()
                if n in categories:
                    categories[n] += 1
                else:
                    categories[n] = 1
            else:
                no_cat_value.append(i)

    print 'Number of no categories keys =', len(no_cat_key)
    print 'Number of categories with empty data = ', len(no_cat_value)
    #print 'Category dict ', categories
    print 'Len cat dict =', len(categories)

def sellerInfo(json_data_list):
    seller_dict = {}
    no_seller_key = []
    no_seller_name = []

    for i, jsond in enumerate(json_data_list):
        if 'seller' not in jsond:
            no_seller_key.append(i)
            continue
        if 'name' not in jsond['seller']:
            no_seller_name.append(i)
            continue
        
        sname = jsond['seller']['name'].encode('ascii', 'ignore').lower()
        if sname in seller_dict:
            seller_dict[sname] += 1
        else:
            seller_dict[sname] = 1
        
    print 'seller_dict =', seller_dict
    print 'unique sellers = ', len(seller_dict)
    print 'no seller key items = ', len(no_seller_key)
    print 'no seller name items = ', len(no_seller_name)
    
def main ():
    product_json_filename = sys.argv[1]
    category_json_filename = sys.argv[2]
    includeList(category_json_filename)
    return 0
    json_data_list = productsAsJson(product_json_filename)
    #sellerInfo(json_data_list)
    #categoryInfo(json_data_list)
    alternateProductCat(json_data_list)
    

if __name__ == "__main__":
    main()
