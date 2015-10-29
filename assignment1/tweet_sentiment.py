import sys
import json
from pandas import DataFrame, Series
import pandas as pd

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))



def comparefile(comparefile1, records0):
#    records = [json.loads(line) for line in tweet_file]
    frame = DataFrame(records0)
    tweet = frame['text']

    tweet = tweet.dropna()
    print(tweet[:10])
    df1 = DataFrame(tweet)
    df1.index=range(len(df1))
    df1['score'] = 0
#    columns=['word', 'affinity']
#    comparefile = pd.read_table(aff_file, sep='\t', names = columns)
    comparefile1['sentence']=0
    
    for word in comparefile1['word']:
        if ' ' in word:
            #comparefile1.sentence[comparefile1['word']==word]=1
            comparefile1.loc[comparefile1['word']==word, 'sentence']=1

    comparefile_sort = comparefile1.sort_index(by = 'sentence', ascending = False)

    comparefile_two_word = comparefile_sort[comparefile_sort.sentence==1]
    affinity_two_word = comparefile_two_word.affinity
    comparefile_one_word = comparefile_sort[comparefile_sort.sentence==0]
    affinity_one_word = comparefile_one_word.affinity
    
    for j in range(len(df1)):
        text = df1.text[j].split(' ')
        for word in text:
            if (comparefile_one_word.word==word.lower()).any():
                df1.score[j]+= affinity_one_word[comparefile_one_word.word==word.lower()]
                #df1.ix[j, 'score']+= affinity_one_word[comparefile_one_word.word==word.lower()]
            
        

    for j in range(len(df1)):
        text = df1.text[j].split(' ')
        for k in range(len(text)-1):
            if (comparefile_two_word.word==(text[k].lower()+' '+text[k+1]).lower()).any():
                df1.score[j]+= affinity_two_word[(comparefile_two_word.word==(text[k].lower()+' '+text[k+1].lower()))]
                #Df1.ix[j, 'score']+= affinity_two_word[(comparefile_two_word.word==(text[k].lower()+' '+text[k+1].lower()))]
    
    return df1




def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
#    lines(sent_file)
#    lines(tweet_file)
    records = [json.loads(line) for line in tweet_file]
    columns=['word', 'affinity']
    comfile1 = pd.read_table(sent_file, sep='\t', names = columns)
    hw()

    df2 = comparefile(comfile1, records)
    print(df2.score[:10])
    temp = sys.stdout #store original stdout object for later
    sys.stdout = open('log1.txt','w') #redirect all prints to this log file
#    print("testing123") #nothing appears at interactive prompt
    for score in df2.score:
        print(score)
   

    sys.stdout = temp #restore print commands to interactive prompt
    print("back to normal") #this shows up in the interactive prompt




if __name__ == '__main__':
    main()
