'''
Create the brand and seller cloud.
Takes in the products json data
output the sorted cloud to 
products.brandcloud
products.sellercloud
'''

import os
import sys

from brandsLoader import updateBrand, updateSeller, extractSeller
from productLoader import productsAsJson
from utils import sort_dict

def writeBrands(brands, filename):
    f = open(filename, 'w')
    
    for b in brands:
        name, count = b
        f.write(name)
        f.write(',')
        f.write(str(count))
        f.write("\n")
    f.close()
    
def updateUnknownBrands(product, unknown_brand_sellers):
    seller = extractSeller(product)
    if seller is None:
        unknown_brand_sellers['unknown'] += 1
    else:
        if seller not in unknown_brand_sellers:
            unknown_brand_sellers[seller] = 1
        else:
            unknown_brand_sellers[seller] += 1
        
def main():
    if len(sys.argv) < 2:
        print __file__, 'products.json'
    
    products_jsonfile = sys.argv[1]
    
    brands_filename = os.path.splitext(products_jsonfile)[0] + ".brandcloud"
    sellers_filename = os.path.splitext(products_jsonfile)[0] + ".sellercloud"
    
    products = productsAsJson(products_jsonfile)
    
    print 'Loaded ', len(products), 'products'
    
    brands = {'unknown': 0}
    sellers = {'unknown': 0}
    
    unknown_brand_sellers = {'unknown': 0}
    
    for i, product in enumerate(products):
        brand_found = updateBrand(product, brands)
        updateSeller(product, sellers)
        
        if not brand_found:
            updateUnknownBrands(product, unknown_brand_sellers)
            
                    
    brands_sorted = sort_dict(brands, reverse = True)
    writeBrands(brands_sorted, brands_filename)
    print 'Written file ', brands_filename
    
    sellers_sorted = sort_dict(sellers, reverse=True)
    writeBrands(sellers_sorted, sellers_filename)
    print 'Written file ', sellers_filename
    
    print 'Sellers of products which does not have a brand tagged', unknown_brand_sellers
    
main()

    