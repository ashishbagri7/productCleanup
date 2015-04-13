'''
Loads into memory the initial category list
each element in the list is a json object with keys:
catname_en, catname_ind, catset_en, catset_ind
etype = category specified if its a category or not (so to use or not)

During categorization, 
    takes in a product data
    uses the keys: description, title, categories/name 
    parses values in these fields. compares with all existing categories and if there is a match, 
    out the catname_en, catname_ind for it
        
'''

# dealing with plurals
from collections import Counter
import json
import logging
import sys
import time

from categoryCalculator import categorizeProduct
from categoryLoader import loadCategories
from productLoader import productsAsJson

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

weights = {"categories":1.0, "title": 0.75, "description": 0.5}

'''
Applying weights to the different tags:
First level weighting is done by the counts of the tags,
They are weighted between max -> 1.0 and min -> count/max
Second level of weighting is done depending upon where the tag was found.
tags found in categories is ranked higher than tags found in title which is higher than tags in description
'''
def weightedTags(final_tags, category_found):    
    final_tags_counter = Counter(final_tags)
    tags_sorted = final_tags_counter.most_common()
    total_tags_count = sum(final_tags_counter.values())
    max_tag_count = max(final_tags_counter.values())
    tags_weighted = []
    for tag, tagcount in tags_sorted:
        if tag in category_found['categories']:
            tags_weighted.append((tag, float(tagcount)*weights['categories'] / max_tag_count))
        elif tag in category_found['title']:
            tags_weighted.append((tag, float(tagcount)*weights['title'] / max_tag_count))
        else:
            tags_weighted.append((tag, float(tagcount)* weights['description'] / max_tag_count))
    
    
    tags_weighted = sorted(tags_weighted, key=lambda tup: tup[1], reverse = True)
    return tags_weighted

def getProductTagsDict(tags_weighted, category_db):
    product_tags = {'product_tags': []}
    # each tag is of this structure
    # {'tag_en': "", 'tag_ind': "", 'weight': 0}
    
    for tagid, tagweight in tags_weighted:
        tag_info = {'en': category_db[tagid]['catname_en'], \
                    'ind': category_db[tagid]['catname_ind'], \
                    'weight': tagweight \
                    }

        product_tags['product_tags'].append(tag_info)

    return product_tags

'''
Take in a product json and return the tags found for this product.
The tags are form of dict and are weighted and orderd
'''
def productCategory(pid, product_json, category_db):
    global overall_tags_count
    category_found = {'description': [], 'title': [], 'categories': []}
    
    category_found, _ = categorizeProduct(product_json, category_db)
    
    logging.info('%s) Pid: %s : %s' % (str(pid), product_json['id'], json.dumps(category_found)))
    
    # Need a final category list
    final_tags = []
    final_tags.extend(category_found['description'])
    final_tags.extend(category_found['title'])
    final_tags.extend(category_found['categories'])
    
    # if there are tags !
    if len(final_tags):
        tags_weighted = weightedTags(final_tags, category_found)
        logging.info("%s) Pid: %s : Tags weighted %s" % (str(pid), product_json['id'], json.dumps(tags_weighted)))
        return getProductTagsDict(tags_weighted, category_db)
    else:
        return {'product_tags': []}

def printhelp():
    print __file__, 'TagsJson', 'productsJson', 'outputfile'
    sys.exit(1)
    
def main():
    if len(sys.argv) < 4:
        printhelp()
        
    category_file = sys.argv[1]
    products_file = sys.argv[2]
    output_file = sys.argv[3]
    
    category_db = loadCategories(category_file)
    print 'Number of category tags: ', len(category_db)
        
    products = productsAsJson(products_file)
    total_products = len(products)
    print 'Number of products : ', total_products
        
    print 'The output file is ', output_file
    
    print 'Applying following weights to sections ', weights
    
    products_updated = []
    tag_found_for = 0
    
    product_tag_count = []
    
    
    start = time.time()
    for i, product in enumerate(products):
        if i and i % 100 == 0:
            print 'Completed ', i, 'out of ', total_products
            
        product_tag = productCategory(i, product, category_db)

        if product_tag is not None:
            product_tag_count.append((i, len(product_tag['product_tags'])))
            product.update(product_tag)
            products_updated.append(product)
            if len(product_tag['product_tags']):
                tag_found_for += 1
        else:
            logging.error("NO products found for id: " + str(i))
            product_tag_count.append((i,0))
                            
    end = time.time()
    
    print 'Average time per product assignment (in mili secs) : ', ((end - start)*1000.0) / total_products
    print 'Tags found for %d out of %d products' % (tag_found_for, total_products)
    
    print 'Products with maximum tags:'
    product_tag_count = sorted(product_tag_count, key=lambda tup: tup[1], reverse = True)
    print product_tag_count[0:100]
        
    json.dump(products_updated, open(output_file, 'w'))
    print 'Written updated products json in file ', output_file

main()
