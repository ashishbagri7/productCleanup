
from collections import OrderedDict
import json
from wordsManipulator import entity2words


# Include set loads up the category json file supplied by sarp
def includeCategories(category_json_file):
    init_category_set = set ()
    product_categories = categoryList(category_json_file)
    for p in product_categories:
        # add the p['name'] to the set
        cnames = p['name'].encode('ascii', 'ignore').rstrip().lower().split(" ")
        for cname in cnames:
            init_category_set.add(cname)
                
        # add all products from the english translation
        if 'values_en' in p:
            for p_en in p['values_en']:
                ennames = p_en.encode('ascii', 'ignore').rstrip().lower().split(" ")
                for enname in ennames:
                    init_category_set.add(enname)
        
        if 'values_ind' in p:
            for p_ind in p['values_ind']:
                indnames = p_ind.encode('ascii', 'ignore').rstrip().lower().split(" ")
                for indname in indnames:
                    init_category_set.add(indname)
        
    return init_category_set

def categoryList(category_json_file):
    with open(category_json_file) as f:
        datastr = f.read()
        category_list = json.loads(datastr)
    
    return category_list


'''
Gets the individual elements from the category field
'''
def categoryItems(category_field):
    category_items = []
    for c in category_field:
        if 'name' in c:
            x = entity2words(c['name'])
            category_items.append(x)

    return category_items


'''
Loads the categories (tags) json database

'''
def loadCategories(category_file, include_counts = False):
    with open(category_file) as f:
        category_list_all = json.loads(f.read())

    category_db = OrderedDict()

    for cat in category_list_all:
        cat_dict = {}
        cat_dict['catname_ind'] = cat['catname_ind']
        cat_dict['catname_en'] = cat['catname_en']
        cat_dict['cat_id'] = int(cat['cat_id'])
        cat_dict['catset_en'] = set(cat['catset_en'])
        cat_dict['catset_ind'] = set(cat['catset_ind'])
        
        if include_counts:
            cat_dict['catset_en_count'] = dict((el,0) for el in cat_dict['catset_en']) 
            cat_dict['catset_ind_count'] = dict((el,0) for el in cat_dict['catset_ind'])
            cat_dict['cat_count'] = 0
        
        category_db[cat_dict['cat_id']] = cat_dict

    return category_db