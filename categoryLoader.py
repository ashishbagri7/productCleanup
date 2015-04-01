
import json

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
