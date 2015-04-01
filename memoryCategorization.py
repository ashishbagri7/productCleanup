from cgitb import enable
from PyDictionary.test_pydictionary import dictionary

## takes in information it knows
## dumps a json for all the known categories

'''
Algorithm for the memory Classification

everything is a set and lower case

1, Load the category json data set
    en_words, id_words, common_category
    need to expand this set::
    for each en_word: find synonyms and add them to a set
    for common category: add them to the english set with its synonyms
    for each element in that set, translate the data to id and add them to a set
    add the existing data of id into the same set
    
    data is transformed to ::
    "etype": "category" 
    cat_en    
    cat_id
    name_en
    name_id
    
    create a dict object for each of the category ! 
    
    >> How to get duplicates and remove them !?
    name_en -> should be unique !
    names_id -> may/maynot be unique
    
    
    
    PyDictionary

    # while guessing the categories.. check for punctuations and take a decision of what matches
    
    loop over each of the baseline categories:
    for each category:: 
    check if the product belongs to the given category !:: build logic around this  
    

'''
import sys
import json
from PyDictionary import PyDictionary  
from categoryLoader import categoryList

def getSynonym(dictionary, word):
    syns = dictionary.synonym(word)
    try:
        if syns is not None:
            return syns
        else:
            return []
    except Exception as e:
        print 'Cannot find synonyms for %s. Error: %s'%(word, str(e))

def translate_ind(dictionary, word):
    return getTranslation(dictionary, word, "id")

def getTranslation(dictionary, word, language):
    try:
        translated = dictionary.translate(word, language)
        if translated is not None and len(translated) > 0:
            return translated
        else:
            return None
    except Exception as e:
        print 'Cannot translate  %s in %s. Error: %s'%(word, language, str(e))
        return None
    
def asciiLowerHyphens(word):
    return word.encode('ascii', 'ignore').rstrip().lower().replace(" ", "-")
    
def processIndividualCategory(cat_json, dictionary):
    category_dict = {}
    
    catset_en = set()
    catset_id = set()
    
    catname_en = asciiLowerHyphens(cat_json['name'])
    
    print 'catname_en', catname_en
    catset_en.add(catname_en)
    
    if 'values_en' in cat_json:
        for p_en in cat_json['values_en']:
            w_en = asciiLowerHyphens(p_en)
            catset_en.add(w_en)
            w_syn = getSynonym(dictionary, w_en)
            for w in w_syn:
                catset_en.add(asciiLowerHyphens(w))   
    
    if 'values_ind' in cat_json:
            for p_ind in cat_json['values_ind']:
                catset_id.add(asciiLowerHyphens(p_ind))
    
    
    # get the translation of catname_en
    catname_id = translate_ind(dictionary, catname_en)
    if catname_id is not None:
        catname_id = asciiLowerHyphens(catname_id)
    else:
        catname_id = catname_en
    
    print 'catname_id', catname_id
    catset_id.add(catname_id)
    # Add translations of all en values to catset_id
    for w in catset_en:
        l = translate_ind(dictionary, w)
        if l is not None:
            catset_id.add(asciiLowerHyphens(l))
                
    category_dict['catname_en'] = catname_en
    category_dict['catname_id'] = catname_id
    category_dict['catset_en'] = catset_en
    category_dict['catset_id'] = catset_id
    category_dict['etype'] = "category"
    return category_dict

def usage():
    print __file__, 'product_json_file', 'train_id_file'
    sys.exit(1)
    
def main():
    category_json_file = sys.argv[1]
    output_file = sys.argv[2]
    
    
    dictionary=PyDictionary()
    
    category_list = categoryList(category_json_file)
    
    updated_category_list = []
    for l in category_list:
        updated_category_list.append(processIndividualCategory(l, dictionary))
        
    json.dump(updated_category_list, open(output_file, 'w'))
    
if __name__ == "__main__":
    main()
