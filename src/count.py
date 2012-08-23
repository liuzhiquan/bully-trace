
yes, no, tbd = 0, 0, 0

for line in open('labeledTweets2').readlines():
    elems = line.strip().split('\t')
    if len(elems) == 3:
        if elems[2] == 'yes':
            yes += 1
        elif elems[2] == 'no':
            no += 1
        elif elems[2] == 'tbd':
            tbd += 1

print 'yes=%d, no=%d, tbd=%d' % (yes, no, tbd)