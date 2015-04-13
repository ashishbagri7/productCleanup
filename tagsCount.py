import json
import sys
'''
Reads in products json file with updated product_tags
Helpful for debugging if some products have very large number of tags
'''

product_json_file = sys.argv[1]

products = json.load(open(product_json_file))

tags_count = {}
tags_dict = {}

def update_count(c):
    if c not in tags_count:
        tags_count[c] = 1
    else:
        tags_count[c] += 1

for p in products:
    if 'product_tags' in p:
        prod = p['product_tags']
        update_count(len(prod))
        if len(prod) > 20:
            print p['title']
            print p['description']
            print p['product_tags']
            print '****************'
        
        for t in prod:
            if t['en'] not in tags_dict:
                tags_dict[t['en']] = 1
            else:
                tags_dict[t['en']] += 1
    else:
        update_count(0)
    
print tags_dict
print tags_count
