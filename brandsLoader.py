

from wordsManipulator import ignorePunctuations, asciiLower, stripPunctuations

def updateBrand(p, brands):
    brand_found = False
    if 'brand' in p:
        b = stripPunctuations(asciiLower(p['brand']))
        if len(b) > 0:
            brand_found = True
            if b in brands:
                brands[b] += 1
            else:
                brands[b] = 1                    
    if not brand_found:
        brands['unknown'] += 1
    
    return brand_found
    
    
def extractSeller(p):
    seller = None
    if 'seller' in p:
        if 'name' in p['seller']:
            b = stripPunctuations(asciiLower(p['seller']['name']))
            if len(b) > 0:
                seller = b
    
    return seller

def updateSeller(p, sellers):    
    seller_found = False
    seller = extractSeller(p)
    
    if seller is not None:
        seller_found = True
        if seller in sellers:
            sellers[seller] += 1
        else:
            sellers[seller] = 1
    else:
        sellers['unknown'] += 1
        
    return seller_found
