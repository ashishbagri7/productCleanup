
'''
def read_trainfile(train_filename):
    categorySet = set()
    
    with open(train_filename) as f:
        for line in f:
            line = line.rstrip()
            if len(line) > 0:
                name, cat = line.split("\t")
                if cat != "0":
                    categorySet.add(name)
    
    return categorySet     
'''
'''
def readCatProducts(product_json, train_ids):
    categorySet = set()
    
    for i, d in enumerate(product_json):
        if i in train_ids:
            cat_set = categoryItems(d['categories'])
            if len(cat_set) > 0:
                categorySet = categorySet.union(cat_set)
    
    return categorySet
'''
