import sys

f = open(sys.argv[1])

allterms = []
counts = []

count_threshold = 10

for line in f:
    term_count = line.rstrip().split(',')
    if len(term_count) == 2:
        if int(term_count[1]) >= count_threshold:
            allterms.append((term_count[0], int(term_count[1])))
            counts.append(int(term_count[1]))
            
    
f.close()

allterms_sorted = sorted(allterms, key=lambda tup: tup[1], reverse = True)

maxcount = allterms_sorted[10][1]
mincount = allterms_sorted[-1][1]

print maxcount, mincount

f1 = open(sys.argv[1]+'.scaled', 'w')
for e in allterms_sorted:
    if e[1] >= maxcount:
        scaledvale = 1.0
    else:
        scaledvale = float(e[1]) / maxcount
    scaledvale = scaledvale*100.0
    f1.write(','.join([e[0], str(scaledvale)]))
    f1.write('\n')

f.close()
