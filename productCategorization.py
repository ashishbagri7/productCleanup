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
from collections import OrderedDict
import json
import logging
import re
import string
import sys

from productLoader import productsAsJson


logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
category_db = None

# exclude_punctuation = set(string.punctuation)
# exclude_punctuation.add(" ")
# strip_punctuation = ''.join(exclude_punctuation)
# testsection = "adahf-fah faj afha!\n fah-f ffa.fa"

# take an entity: could be description, title, catgories
# makes it into a list of list with all the individual words
# stripped out of all punctuations
def entity2words(entity):
    # convert to ascii and lower it
    entity = asciiLower(entity)
    # split it to individual lines
    lines = entity.split("\n")
    return_list = []
    # for each line, there must be a list
    for line in lines:
        x = re.split('\W+', line)
        x = filter(None, x)
        if len(x):
            return_list.append(x)

    # list of list
    return return_list

def entity2category(entity_list):
    # entity_list is a list of list
    category_found = []
    for line in entity_list:
        cf = getCommonCategory(line)
        if len(cf):
            category_found.extend(cf)
            cdebug = [(category_db[cid]['catname_en'], category_db[cid]['catname_ind']) for cid in cf]
            logging.debug("%s --> %s" % (json.dumps(line), json.dumps(cdebug)))

    return category_found

def categoryItems(category_field):
    category_items = []
    for c in category_field:
        if 'name' in c:
            x = entity2words(c['name'])
            category_items.append(x)

    return category_items


def loadCategories(category_file):
    with open(category_file) as f:
        category_list_all = json.loads(f.read())

    category_db = OrderedDict()

    for cat in category_list_all:
        cat_dict = {}
        # TODO: Should convert to ascii here too ?
        if 'etype' in cat and cat['etype'] == "category":
            cat_dict['catname_ind'] = cat['catname_ind']
            cat_dict['catname_en'] = cat['catname_en']
            cat_dict['cat_id'] = cat['cat_id']
            cat_dict['catset_en'] = set(cat['catset_en'])
            cat_dict['catset_ind'] = set(cat['catset_ind'])
            category_db[cat['cat_id']] = cat_dict

    return category_db

def asciiLower(mystring):
    return mystring.encode('ascii', 'ignore').rstrip().lower()

def compareCategory(word_list, catname):
    # split catname by "-".
    # can be certain that the names do not have spaces or other punctuations
    catnameparts = catname.split("-")
    if set(catnameparts).issubset(set(word_list)):
        return True
    else:
        return False

def getCommonCategory(word_list):
    category_found = []
    # get the categories from these word set
    for cat_id in category_db:
        category = category_db[cat_id]

        cat_match = False
        # for each element in catset_en
        if not cat_match:
            for ele in category['catset_en']:
                if compareCategory(word_list, ele):
                    # found the category
                    cat_match = True
                    break
        if not cat_match:
            for ele in category['catset_ind']:
                if compareCategory(word_list, ele):
                    # found the category
                    cat_match = True
                    break

        if cat_match:
            category_found.append(cat_id)
            # (category['catname_en'], category['catname_ind'])

    return category_found

def categorizeProduct(pid, product_json):
    category_found = {'description': [], 'title': [], 'categories': []}

    if 'description' in product_json:
        descr_list = entity2words(product_json['description'])
        category_found['description'].extend(entity2category(descr_list))

    if 'title' in product_json:
        title_list = entity2words(product_json['title'])
        category_found['title'].extend(entity2category(title_list))

    if 'categories' in product_json:
        # deal with categories differently due to its structure
        clist = categoryItems(product_json['categories'])
        for l in clist:
            category_found['categories'].extend(entity2category(l))


    logging.info('%s) Pid: %s : %s' % (str(pid), product_json['id'], json.dumps(category_found)))

    # Need a final category list
    final_tags = []
    final_tags.extend(category_found['description'])
    final_tags.extend(category_found['title'])
    final_tags.extend(category_found['categories'])

    # if there are tags !
    if len(final_tags):
        final_tags_counter = Counter(final_tags)
        tags_sorted = final_tags_counter.most_common()
        total_tags_count = sum(final_tags_counter.values())
        max_tag_count = max(final_tags_counter.values())

        tags_weighted = []
        for tag, tagcount in tags_sorted:
            tags_weighted.append((tag, float(tagcount) / max_tag_count))

        logging.info("%s) Pid: %s : Tags sorted %s" % (str(pid), product_json['id'], json.dumps(tags_sorted)))
        logging.info("%s) Pid: %s : Tags weighted %s" % (str(pid), product_json['id'], json.dumps(tags_weighted)))

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
    else:
        return {'product_tags': []}

def main():
    global category_db
    category_db = loadCategories(sys.argv[1])
    products = productsAsJson(sys.argv[2])
    output_file = sys.argv[3]

    products_updated = []
    tag_found_for = 0
    tag_tried_for = 0

    for i, product in enumerate(products):
        tag_tried_for += 1
        product_tag = categorizeProduct(i, product)

        if product_tag is not None:
            product.update(product_tag)
            products_updated.append(product)
            print product_tag
            if len(product_tag['product_tags']):
                tag_found_for += 1

    print 'Tags found for %d out of %d products' % (tag_found_for, tag_tried_for)
    json.dump(products_updated, open(output_file, 'w'))

main()
