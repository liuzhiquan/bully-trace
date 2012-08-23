
import sys

countYes, countNo = 0, 0

f_pos_tweets = open('1.txt').readlines()
f_neg_tweets = open('0.txt').readlines()
f1 = open('1.out')
f0 = open('0.out')

tp, tn, fp, fn = 0, 0, 0, 0

f_tp = open('tp.txt', 'w')
f_fp = open('fp.txt', 'w')
f_tn = open('tn.txt', 'w')
f_fn = open('fn.txt', 'w')

for i,line in enumerate(f1.readlines()):
    label = float(line)
    if label > 0:
        tp += 1
        print >> f_tp, f_pos_tweets[i]
    elif label < 0:
        fp += 1
        print >> f_fp, f_pos_tweets[i]


for i,line in enumerate(f0.readlines()):
    label = float(line)
    if label < 0:
        tn += 1
        print >> f_tn, f_neg_tweets[i]
    elif label > 0:
        fn += 1
        print >> f_fn, f_neg_tweets[i]



print 'tp=%d, tn=%d, fp=%d, fn=%d' % (tp, tn, fp, fn)
prec = 1.0 * tp / (tp + fp)
recall = 1.0 * tp / (tp + fn)
f1 = 2 * prec * recall / (prec + recall)
print 'prec=%f, recall=%f, f1=%f' % (prec, recall, f1)
print 'accuracy = %f' % (1.0 * (tp + tn) / (tp + tn + fp + fn))
