
import json
import re

def productsAsJson(filename, N=None):
    json_data_list = []
    num_loaded = 0
    
    with open(filename) as f:
        for line in f:
            data = json.loads(line.strip())
            json_data_list.append(data)
            num_loaded += 1
            if N is not None:
                if num_loaded >= N:
                    break
    
    return json_data_list

def categoryWords(category_list):
    
    category_words_set = set()
    for c in category_list:
        if 'name' in c:
            # category words all !
            cnamelist = c['name'].encode('ascii', 'ignore').rstrip().lower().split(" ")
            for cword in cnamelist:
                category_words_set.add(cword)
    
    return category_words_set

def categoryItems(category_list):
    category_items_set = set()
    for c in category_list:
        if 'name' in c:
            # category words all !
            cname = c['name'].encode('ascii', 'ignore').rstrip().lower()
            category_items_set.add(cname)
    
    return category_items_set


def descriptorWords(descriptorText):
    desc_lines = descriptorText.rstrip().encode('ascii', 'ignore').split("\n")
    desc_words = []
    # for each description line     
    for dline in desc_lines:
        # get words in the descp line
        dwords = re.findall(r"[\w']+|[.,!?;]", dline.rstrip())
        desc_words.extend(dwords)
        '''
        dwords = dline.split(" ")
        # for each word in the line
        for w in dwords:
            desc_words.append(w)
            #w = cleanPuntuation(w)
            #if len(w) > 1:
            #desc_words.append(w)
        '''
            
    return desc_words