# # takes in information it knows
# # dumps a json for all the known categories

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
from PyDictionary import PyDictionary
from collections import OrderedDict
import json
from nltk.corpus import wordnet as wn
import sys

from categoryLoader import categoryList

stop_words = set({'top'})
# stop_category = set(['face', 'lips'])
stop_category = set(['face'])

# TODO: find a way to make this only consider noun synonyms !
# trying to use nltk
# can return the same word as a syn
# # replace '_' with '-'

def getSynonym_nlk(word):
    try:
        wnsyns = wn.synsets(word, pos=wn.NOUN)
        syns = set()
        for s in wnsyns:
            x = asciiLowerHyphensUnderscore(s.name()).split(".")[0]
            if x != word and x not in stop_words:
                syns.add(x)

        return list(syns)
    except Exception as e:
        print e
        return []

def getSynonym(dictionary, word):
    syns_temp = dictionary.synonym(word)
    syns = set()
    try:
        if syns_temp is not None:
            for s in syns_temp:
                if s not in stop_words:
                    syns.add(s)

            return list(syns)
        else:
            return []
    except Exception as e:
        print 'Cannot find synonyms for %s. Error: %s' % (word, str(e))
        return []

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
        print 'Cannot translate  %s in %s. Error: %s' % (word, language, str(e))
        return None

def asciiLowerHyphens(word):
    return word.encode('ascii', 'ignore').rstrip().lower().replace(" ", "-")

def asciiLowerHyphensUnderscore(word):
    return word.encode('ascii', 'ignore').rstrip().lower().replace(" ", "-").replace("_" , "-")


def processIndividualCategory(cat_id, cat_json, dictionary):
    original_count_en = 1
    original_count_ind = 0
    
    category_dict = OrderedDict()
    catset_en = set()
    catset_id = set()

    catname_en = asciiLowerHyphens(cat_json['name'])
    if catname_en in stop_category:
        print 'Ignoring category ', catname_en
        return None

    print 'Catname orig %s updated %s' % (cat_json['name'], catname_en)
    catset_en.add(catname_en)

    if 'values_en' in cat_json:
        original_count_en += len(cat_json['values_en'])
        for p_en in cat_json['values_en']:
            w_en = asciiLowerHyphens(p_en)
            catset_en.add(w_en)
            # w_syn = getSynonym(dictionary, w_en)
            w_syn = getSynonym_nlk(w_en)
            for w in w_syn:
                catset_en.add(asciiLowerHyphens(w))

    if 'values_ind' in cat_json:
        original_count_ind += len(cat_json['values_ind'])
        for p_ind in cat_json['values_ind']:
            catset_id.add(asciiLowerHyphens(p_ind))

    # get the translation of catname_en
    catname_ind = translate_ind(dictionary, catname_en)
    if catname_ind is not None:
        catname_ind = asciiLowerHyphens(catname_ind)
    else:
        catname_ind = catname_en

    catset_id.add(catname_ind)
    # Add translations of all en values to catset_id
    for w in catset_en:
        l = translate_ind(dictionary, w)
        if l is not None:
            catset_id.add(asciiLowerHyphens(l))

    category_dict['etype'] = "category"
    category_dict['cat_id'] = cat_id
    category_dict['catname_en'] = catname_en
    category_dict['catname_ind'] = catname_ind
    category_dict['catset_en'] = list(catset_en)
    category_dict['catset_ind'] = list(catset_id)
    
    added_en = len(category_dict['catset_en']) - original_count_en
    added_id = len(category_dict['catset_ind']) - original_count_ind
    return category_dict, added_en, added_id

def usage():
    print __file__, 'product_json_file', 'train_id_file'
    sys.exit(1)

def main():
    category_json_file = sys.argv[1]
    output_file = sys.argv[2]

    dictionary = PyDictionary()

    category_list = categoryList(category_json_file)
    print 'Original num of categories ', len(category_list)
    total_added_en = 0
    total_added_ind = 0
    updated_category_list = []
    
    for indx, l in enumerate(category_list):
         indCat = processIndividualCategory(indx, l, dictionary)
         if indCat is not None:
            cat_dict, added_en, added_id = indCat
            total_added_en += added_en
            total_added_ind += added_id
            updated_category_list.append(cat_dict)

    print 'Updated num of categories ', len(updated_category_list)
    print 'Total added en ', total_added_en
    print 'Total added ind ', total_added_ind
    json.dump(updated_category_list, open(output_file, 'w'))

if __name__ == "__main__":
    main()
