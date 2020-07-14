import pandas as pd
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from io import StringIO
from tqdm import tqdm
import time

#############################################################################################################################
##################                                                                                         ##################
##################                    Reading in Textfile containing text and ids                          ##################
##################                                                                                         ##################
#############################################################################################################################

continuing_file_path_1_2 = 'D:\\DownloadsDesktop\\Desktop\\Oxford\\FYP\\fyp_collective_emotion\\Data\\wall_sentiment.csv' #This line has to be adjusted to the file that you want to analyse

d_full = pd.read_csv(continuing_file_path_1_2, #loading that dataset
                         error_bad_lines=False,
                         index_col=False,
                         )

pbar = tqdm(total=len(d_full))

lenght_list = [] # this chunk of got gets rid of all troublesome cases, because twitter sometimes has texts bodys that are absrdly long, which we exclude here.
for x in range(len(d_full)):
    lenght_list.append(len(d_full.iloc[x, 3]))
print(len(lenght_list) == len(d_full))
d_full["lenght_list"] = lenght_list
d_full = d_full.loc[d_full['lenght_list'] < 250]

d_full = d_full.iloc[:]
d_full = d_full.reset_index(drop=True)

analyzer = SentimentIntensityAnalyzer()
#for sentence in sentences:
#    vs = analyzer.polarity_scores(sentence)
#    print("{:-<65} {}".format(sentence, str(vs)))

df = pd.DataFrame(columns=['sen_neg', 'sen_neu', 'sen_pos','compound', 'text'])
print(df)

start = time.time() # just as reference
for index, row in d_full.iterrows():
    vs = analyzer.polarity_scores(row[3])
    vs['text'] = row[3]
    df = df.append(vs, ignore_index=True)
    pbar.update(1)

df_v = df.iloc[:,3:8]
df_final = pd.concat([df_v, d_full],  axis=1, sort=False)
df_final = df_final.drop(df_final.columns[[1]], axis=1)

df_final.to_csv('D:\\DownloadsDesktop\\Desktop\\Oxford\\FYP\\fyp_collective_emotion\\Data\\wall_sentiment_vader.csv',index=None, header=True,encoding="utf-8")

end = time.time()
time_taken = end - start
print('Time: ',time_taken)
