Bullying Trace Classifier V1.0
June 2012

This package includes two modules for recognizing bullying traces.  See comments in source files for more details.

--------------------------------------------------------------
Step 1: 
Create a plain text file with the text you want to classify.  Each line is treated as a mini document.
See "test.txt" for an example.

--------------------------------------------------------------
Step 2: 
Run Enrichment.jar to filter the file so as to find lines containing (roughly) bull* keywords. This produces what's called "enriched data".

Example usage:
   cat test.txt | java -jar Enrichment.jar > test_filtered.txt

The file "test.txt" contains 7 example tweets.  The code filters out one tweet "Lauren is a fat cow MOO BITCH" that doesn't contain any of the keywords.

--------------------------------------------------------------
Step 3: 
Run Classification.jar which takes enriched data and classifies each line as bullying trace or not.

Example usage:
   cat test_filtered.txt | java -jar Classification.jar

The code outputs a number (SVM margin), one for each line of text:
   0.42538682884290324
   0.7169217536340691
   1.421481042142981
   1.2759181565336495
   0.19255605948863025
   -0.5733835902347938
By the sign of the margin, the code classified every line as a bullying trace except the last line ("Forced veganism ..."), which indeed is not about bullying.

--------------------------------------------------------------
Citation:

Learning from bullying traces in social media
Jun-Ming Xu, Kwang-Sung Jun, Xiaojin Zhu, and Amy Bellmore
In North American Chapter of the Association for Computational Linguistics - Human Language Technologies (NAACL HLT)
Montreal, Canada, 2012

Contact: Jun-Ming Xu (xujm@cs.wisc.edu), Xiaojin Zhu (jerryzhu@cs.wisc.edu)
