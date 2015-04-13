
'''
Generate the product tags cloud and autocompletion list

Count of products associated with each tag and sub tags

Takes as input the tag chart file, product json and output file
The output is a csv of the tag chart with all the counts with the tags       
'''

#from collections import Counter
#from collections import OrderedDict
import json
import logging
import sys

from categoryCalculator import updateTags
from categoryLoader import loadCategories
from productLoader import productsAsJson


logging.basicConfig(stream=sys.stdout, level=logging.ERROR)


''' 
dump the tag cloud to file
'''
def writeTagCloud(tagoutfile, category_db):
    out = open(tagoutfile+'.csv', 'w')
    
    for cid in category_db:
        category = category_db[cid]
        
        x = ['cat_id', str(cid)]
        out.write(','.join(x))
        out.write("\n")
        
        x = ['catname_en', category['catname_en'], str(category['cat_count'])]
        out.write(','.join(x))
        out.write("\n")
        
        x = ['catname_ind', category['catname_ind'], str(category['cat_count'])]
        out.write(','.join(x))
        out.write("\n")
        
        x = ['catset_en']
        for ele in category['catset_en']:
            x.extend([ele, str(category['catset_en_count'][ele])])
        out.write(','.join(x))
        out.write("\n")
        
        x = ['catset_ind']
        for ele in category['catset_ind']:
            x.extend([ele, str(category['catset_ind_count'][ele])])
        out.write(','.join(x))
        out.write("\n")
        out.write("\n")
            
    out.close()

def printhelp():
    print __file__, 'TagsJson', 'productsJson', 'outputfile'
    sys.exit(1)
    

def createTagCloud(products, category_db):
    total_prod = len(products)
    for i, product in enumerate(products):
        if i and i % 100 == 0:
            print 'Completed ', i, 'out of ', total_prod
        updateTags(i, product, category_db)    


def main():
    if len(sys.argv) < 4:
        printhelp()
        
    category_file = sys.argv[1]
    products_file = sys.argv[2]
    output_file = sys.argv[3]
    
    category_db = loadCategories(category_file, True)
    print 'Number of category tags: ', len(category_db)
            
    products = productsAsJson(products_file)
    print 'Number of products : ', len(products)
    
    print 'The output file is ', output_file
    
    createTagCloud(products, category_db)
    
    print 'Writing tag cloud file'
    writeTagCloud(output_file, category_db)
    print 'Completed writing the file'
        
main()
