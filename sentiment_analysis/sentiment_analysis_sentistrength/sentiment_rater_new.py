# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 23:06:15 2015

@author: danyang
"""
# Batch processing mode:
# java -jar /Users/danyang/Documents/Research/collective_emotoin/twitter/sentiment_analysis/SentiStrength.jar sentidata /Users/danyang/Documents/Research/collective_emotoin/twitter/sentiment_analysis/SentStrength_Data/ input fake_tweets.txt

from subprocess import Popen, PIPE
import os
from datetime import datetime
import shutil
# this code is aimed to reduce the burden of writing so many files on your hard drive.
class SentimentRater:
    def __init__(self):
        self.tweets = []
        self.temp_file = '\\Users\\Amit\\OneDrive\\python\\Twitter_data\\sentiment_analysis\\textforrating.txt'
        self.jar_file = '\\Users\\Amit\\OneDrive\\python\\Twitter_data\\sentiment_analysis\\SentiStrength.jar'
        self.data_file = '\\Users\\Amit\\OneDrive\\python\\Twitter_data\\sentiment_analysis\\SentiStrength_Data\\'

    def AddTweetObject(self, tweet):
        self.tweets.append(tweet)
    def CalculateSentiment(self):
        #tweet_tuple = (tweet_id, user_id, post_time, time_bin_s, nr_entry, tweetbody, isRetweet, favourite_count, retweet_count)
        # Step 1: write tweets into a plain text file on disk.
        count_line = 0
#        print 'len of tweets:' , str(len(self.tweets))
        with open(self.temp_file, 'w') as f:
            for tweet_object in self.tweets:
                #tweet_body = tweet_object['body'].encode('utf-8')
                count_line = count_line+1
                #tweet_body=tweet_body.replace('\n', ' ').replace('\r', ' ')
#                    tweet_body=re.sub('\s+', ' ', tweet_body)
                tweet_body = tweet_object[9]
                f.write(tweet_body)  #write all tweets
                f.write('\n')

        # Step 2: call the java program to run over the text file.
        jcmd = 'java -jar ' + self.jar_file + ' sentidata ' + self.data_file + ' input ' + self.temp_file
        p = Popen(jcmd , shell=True, stdout=PIPE, stderr=PIPE)
        out_put, err = p.communicate()
        tokens = out_put.split()
        for token in tokens:
            if '.txt' in token:
                senti_file = token
#                print 'senti file name: ', senti_file

        # Step 3: parse the result text file and fill in tweets.
        with open(senti_file) as f:
            first_line = f.readline()

            for i in range(count_line):
                next_line = f.readline()
                if not next_line:
                    print ('empty line found in line#', i)
                line = next_line.split('\t')
                if len(line) != 3:
                    print ('more columns than expected:', next_line)

                senti_line = [line[0], line[1], str(int(line[0])+int(line[1]))]
                # posSenti, negSenti, senti_score
                self.tweets[i] = tuple(list(self.tweets[i]) + senti_line)

#                print 'i:, ', str(i)
#                print 'timebin:', self.tweets[i]['time_bin']
        curr_datetime = str(datetime.now())
        curr_datetime = curr_datetime.replace(' ', '-').replace(':', '-')
        out_dir = '\\Users\\Amit\\OneDrive\\python\\Twitter_data\\sentiment_analysis\\sentiment_files_mysql\\'
        shutil.copy2(senti_file, out_dir)
        name_parts = senti_file.split('\\')
        senti_name = name_parts[-1]
#        print 'senti_name: ', senti_name
#        print out_dir +senti_name
        os.renames(out_dir+senti_name, out_dir+'tweet_batch_sentiment_'+curr_datetime+'.txt')
        os.remove(senti_file)

        return self.tweets

    def ClearTweets(self):
        self.tweets = []

    def ClearTextContent(self):
#        open('textforrating.txt', 'w').close()
        if os.path.isfile(self.temp_file):
            os.remove(self.temp_file)

    def Size(self):
        return len(self.tweets)
