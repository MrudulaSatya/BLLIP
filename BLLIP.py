#BLLIP SCORE CALCULATION CODE#
#Author: Mrudula Y#
#Dated:8th April, 2018#
#Citing reference used for Hindi Dependency Parser:  http://sivareddy.in/downloads#

from __future__ import division
from tables import *
class Treebank(IsDescription):
    idNum = Int64Col()
    word = StringCol(50)
    Head = Int64Col()
h5file = open_file("HDTB", mode="w", title="Hindi file")
group = h5file.create_group("/", 'DepTree', 'Hindi_dependency_treebank')
table = h5file.create_table(group, 'Candidate', Treebank, "Candidate_DTB")
table1 = h5file.create_table(group, 'Reference', Treebank, "Reference_DTB")
print(h5file)
words = table.row
words1 = table1.row

#Replace file name with the name of candidate dependency output file being used
with open('cand.output') as f:
    content = f.readlines()
content = [x.split() for x in content]
f.close()
#Replace file name with the name of reference dependency output file being used
with open('ref.output') as f:
    content1 = f.readlines()
content1 = [x.split() for x in content1]
f.close()
count = 1
refId = -1
for x in range(len(content)):
    if(content[x] == []):
        table.flush()
        table = h5file.root.DepTree.Candidate
        dep_tree = dict()
        for y in table:
            head = y['Head']
            word = y['word']
            z = y['idNum'] + 1
            for row in table.iterrows(start= z):
                if(row['idNum'] == head and head!=0 and row['word'] != word):
                    dep_tree[row['word']] = word
                    break;
        refId = refId + 1
        for ref in range(refId,len(content1)):
            if(content1[ref] == []):
                table1.flush()
                table1 = h5file.root.DepTree.Candidate
                dep_tree1 = dict()
                for refx in table1:
                    head1 = refx['Head']
                    word1 = refx['word']
                    z1 = refx['idNum'] + 1
                    for refy in table1.iterrows(start= z1):
                        if(refy['idNum'] == head1 and head!=0 and refy['word'] != word1):
                            dep_tree1[refy['word']] = word1
                shared_items = set(dep_tree.items()) & set(dep_tree1.items())
                matched = len(shared_items)                
                possibleMatches = x + (ref - matched)
                bllipScore = matched/possibleMatches
                print ("Sentence ",count, ":\n")
                print("No of Matched Dependencies:",matched)
                print("No of Possible Matches:",possibleMatches)
                print("BLLIP Score:", bllipScore)
                print("\n")
                count=count+1
                refId = ref
                break;
            else:
                words1['idNum'] = content1[x][0]
                words1['word'] =  content1[x][1]
                words1['Head'] = content1[x][4]
                words1.append()
        continue;
    else:
        words['idNum'] = content[x][0]
        words['word'] =  content[x][1]
        words['Head'] = content[x][4]
        words.append()
        

   

