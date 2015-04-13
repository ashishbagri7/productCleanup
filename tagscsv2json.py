from collections import OrderedDict
import json
import sys

'''
Convert tags csv from the excel sheet to the json format used by other scripts
'''

def createTagDict(tagdata):
    tagd = OrderedDict()
    for t in tagdata:
        t = filter(None, t.strip().split(","))
        if len(t):
            if t[0] in ['cat_id', 'catname_en', 'catname_ind']:
                tagd[t[0]] = t[1]
            if t[0] in ['catset_en', 'catset_ind']:
                tagd[t[0]] = list(set(t[1:]))
    return tagd

def print_help():
    print __file__, 'tags_csv_file', 'tags_json_file'
    sys.exit(1)

def main():
    if len(sys.argv) < 3:
        print_help()
        
    tag_list = []
    tags_csv = sys.argv[1]
    tags_json_file = sys.argv[2]
    
    f = open(tags_csv)
    data = f.readlines()
    
    #for lineno in range(0, len(data)):
    lineno = 0
    while lineno < len(data):
        line = data[lineno].strip()
        if len(line) and line is not None:
            x = filter(None, line.split(","))
            if len(x) and x[0] == 'cat_id':
                t = createTagDict(data[lineno:lineno + 5])
                if t is not None:
                    tag_list.append(t)
                
        lineno += 1
    
    print 'length of tag list', len(tag_list)
    json.dump(tag_list, open(tags_json_file, 'w'))
    print 'Written the tags json in file ', tags_json_file
    

main()
