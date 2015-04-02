
'''
Loads into memory the initial category list
each element in the list is a json object with keys:
catname_en, catname_id, catset_en, catset_id
etype = category specified if its a category or not (so to use or not)

During categorization, 
    takes in a product data
    uses the keys: description, title, categories/name 
    parses values in these fields. compares with all existing categories and if there is a match, 
    out the catname_en, catname_id for it
        
'''
import sys
import json 
from productLoader import productsAsJson
import string

exclude_punctuation = set(string.punctuation)
exclude_punctuation.add(" ")
strip_punctuation = ''.join(exclude_punctuation)

def categoryItems(category_list):
    category_items_set = set()
    for c in category_list:
        if 'name' in c:
            cname = asciiLower(c['name'])
            cname = cname.strip(strip_punctuation)
            if len(cname):
                category_items_set.add(cname)
    
    return category_items_set


def loadCategories(category_file):    
    with open(category_file) as f:
        category_list_all = json.loads(f.read())
        
    category_list = []
    for cat in category_list_all:        
        cat_dict = {}
        # TODO: Should convert to ascii here too ?
        if 'etype' in cat and cat['etype'] == "category":
            cat_dict['catname_id'] = cat['catname_id'] 
            cat_dict['catname_en'] = cat['catname_en']
            cat_dict['catset_en'] = set(cat['catset_en'])
            cat_dict['catset_id'] = set(cat['catset_id'])
            category_list.append(cat_dict)
    
    return category_list

def asciiLower(mystring):
    return mystring.encode('ascii', 'ignore').rstrip().lower()

def analyseLine(line):
    try:
        # strip off punctuations from start and end of the line    
        words = line.split(" ")
        # strip punctuations from each word of the line
        words = [ i.strip(strip_punctuation) for i in words]
        # remove empty items
        words = filter(None, words)
        return words
    except Exception as e:
        print 'Exception in analysing description line %s. Exception: %s'%(line, str(e))
        return []
    
def analyseSection(section_content):
    # analyse each line of section
    lines = section_content.split("\n")
    word_set = set()
    
    for line in lines:
        if len(line):
            word_set.update(analyseLine(line))
        
    return getCommonCategory(word_set)
    
'''
    checking if a word is a category or not  !
            
''' 
def getCommonCategory(word_set):
    if type(word_set) != set:
        print 'Common categories takes as input a word set'
        return []
    
    category_found = []
    # get the categories from these word set 
    for category in category_list:
        common_en = word_set.intersection(category['catset_en'])
        common_id = word_set.intersection(category['catset_id'])
        if len(common_en) > 0 or len(common_id) > 0:
            #print 'Category found ', category['catname_en'] , category['catname_id'],'Common en ', common_en,'Common id ', common_id
            category_found.append((category['catname_en'], category['catname_id']))
    
    return category_found 
    
def categorizeProduct(pid, product_json, category_list):
        
    category_found = []
    
    if 'categories' in product_json:
        category_found.extend(getCommonCategory(categoryItems(product_json['categories'])))
    
    if len(category_found):
        print pid, 'categories', category_found
        return category_found, 0
        
    if 'title' in product_json:
        title = asciiLower(product_json['title'])
        category_found.extend(analyseSection(title))
    
    if len(category_found):
        print pid, 'title', category_found
        return category_found, 1
        
    if 'description' in product_json:
        descr = asciiLower(product_json['description'])
        category_found.extend(analyseSection(descr))
    
    if len(category_found):
        print pid, 'description', category_found        
        return category_found, 2
    else:
        print pid, 'notfound'
        return None, 3
        
category_list = loadCategories(sys.argv[1])
products = productsAsJson(sys.argv[2])
cat_found_for = 0
cat_tried_for = 0
cat_found_at = {'categories' : 0, 'title': 0, 'description': 0}
for i, product in enumerate(products[0:3]):
    cat_tried_for += 1
    category_found, wherefound = categorizeProduct(i, product, category_list)
    if category_found is not None:
        if len(category_found):
            if wherefound == 0:
                cat_found_at['categories'] += 1
            if wherefound == 1:
                cat_found_at['title'] += 1
            if wherefound == 2:
                cat_found_at['description'] += 1
            cat_found_for += 1

print 'category tried for ', cat_tried_for, ' found: ', cat_found_for
print cat_found_at
