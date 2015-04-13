import json
import sys

'''
Takes in the category json file and dumps it to a csv format
'''

def main():
    tagfile = sys.argv[1]
    out_csvfile = sys.argv[2]
    f = open(tagfile)
    data = json.load(f)
    f.close()
    
    print 'Writing file ', out_csvfile, ' with the tags data to csv format'
    out = open(out_csvfile, 'w')
    
    for tag in data:
        a = ['cat_id',str(tag['cat_id'])]
        b = ['catname_en',str(tag['catname_en'])]
        c = ['catname_ind',str(tag['catname_ind'])]
        d = ['catset_en']
        d.extend(tag['catset_en'])
        e = ['catset_ind']
        e.extend(tag['catset_ind'])
        
               
        out.write(','.join(a))
        out.write('\n')
        out.write(','.join(b))
        out.write('\n')
        out.write(','.join(c))
        out.write('\n')
        out.write(','.join(d))
        out.write('\n')
        out.write(','.join(e))
        out.write('\n')
        out.write('\n')
        
main()
    