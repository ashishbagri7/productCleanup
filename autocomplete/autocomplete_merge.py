import sys

def merge_tags(autocomplete_f1, autocomplete_f2):    
    autocomplete_dict = {}
    with open(autocomplete_f1) as f:
        for line in f:
            word_count = line.rstrip().split(",")
            x = word_count[0]
            if x not in autocomplete_dict:
                autocomplete_dict[x] = None
    
    
    extra_added = 0
    with open(autocomplete_f2) as f:
        num_read = 0
        for line in f:
            num_read += 1
            if num_read > 1000:
                break
            x = line.rstrip().split(",")
            if len(x) < 2:
                continue
            if len(x) >= 4:
                if x[3] == 'X':
                    continue
            
            d = x[0]
            if d not in autocomplete_dict:
                autocomplete_dict[d] = None
                extra_added += 1
    
    for k in autocomplete_dict:
        print k

def printhelp():
    if len(sys.argv) < 3:
        print __file__, 'tags/brands_list', 'top_words_csv'
        sys.exit(1)

def main():
    printhelp()
    merge_tags(sys.argv[1], sys.argv[2])
    
main()