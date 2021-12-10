import pandas as pd
import os
import numpy as np

# Defining files and locations

in_filename = "all_api_sentiment_tweets" + ".csv"
file_location = "data"
out_filename = "all_api_sentiment_tweets" + ".txt"
db_table_name = "agoldenberg_twitter_hook"

# Functions

def csv_reader(in_filename, file_location):
    current_path = os.getcwd()
    relative_file_path = os.path.join(current_path, file_location, in_filename)

    pd.set_option('display.float_format', lambda x: '%.5f' % x)
    pd.set_option('display.max_colwidth', None)
    dtypes = {'user_id': 'str', 'tweet_id': 'str', 'in_reply_to_status': 'str', 'retweeted_status_id': 'str','quoted_status_id': 'str'}

    df = pd.read_csv(relative_file_path,  # reading in the original dataset
                     error_bad_lines=False,
                     index_col=False,
                     dtype=dtypes)

    # dtypes = {'tweet_id': 'str'}
    #
    # df = pd.read_csv(relative_file_path,  # reading in the original dataset
    #                  error_bad_lines=False,
    #                  index_col=False,
    #                  dtype=dtypes)
    #df.update(df.select_dtypes(include=np.number).applymap('{:,g}'.format)) # remove trailing 0s
    df = df.convert_dtypes()
    return df

def indexer(df):
    df.reset_index(inplace=True, drop=True)
    filter_col = [col for col in df if not col.startswith('Unnam')
                  and not col.startswith('X')
                  and not col.startswith('inserted_at')
                  and not col.startswith('id')] # remove unwanted columns
    df = df[filter_col]
    print("indexer "+ df.columns)
    if 'created_at' in df.columns:
        df.loc[:,'created_at'] = pd.to_datetime(df['created_at'])

    df.loc[:,'inserted_at'] = pd.Timestamp.now()
    df.loc[:,'id'] = df.reset_index().index
    return df

def command_builder(df,db_table_name):
    build_command = "create table " + db_table_name + " ("
    string_col_commands = ""
    col_command = ""
    for col in df:
        if col == "id":
            col_name = col
            SQL_datatype = "int,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "user_id":
            col_name = col
            SQL_datatype = "BIGINT,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "username":
            col_name = col
            SQL_datatype = "TINYBLOB,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "displayname":
            col_name = col
            SQL_datatype = "TINYBLOB,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "inserted_at":
            col_name = col
            SQL_datatype = "DATE,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "link_image":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "summary_bio":
            col_name = col
            SQL_datatype = "MEDIUMBLOB,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "created_at":
            col_name = col
            SQL_datatype = "DATE,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "followers_count":
            col_name = col
            SQL_datatype = "int,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "created_at":
            col_name = col
            SQL_datatype = "DATE,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "statuses_count":
            col_name = col
            SQL_datatype = "int,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "friends_count":
            col_name = col
            SQL_datatype = "int,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "favorites_count":
            col_name = col
            SQL_datatype = "int,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "listed_count":
            col_name = col
            SQL_datatype = "int,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "verified":
            col_name = col
            SQL_datatype = "TINYTEXT,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "lang":
            col_name = col
            SQL_datatype = "TINYTEXT,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "location":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "tweet_id":
            col_name = col
            SQL_datatype = "BIGINT,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "source":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "text":
            col_name = col
            SQL_datatype = "MEDIUMBLOB,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "text_hashtags":
            SQL_datatype = "text,"
            col_name = col
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "text_user_mentions":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "possibly_sensitive":
            col_name = col
            SQL_datatype = "TINYTEXT,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "retweet_count":
            col_name = col
            SQL_datatype = "int,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "in_reply_to_status_id":
            col_name = col
            SQL_datatype = "BIGINT,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "in_reply_to_user_id":
            col_name = col
            SQL_datatype = "BIGINT,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "retweeted_status":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "retweeted_status_id":
            col_name = col
            SQL_datatype = "BIGINT,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "retweeted_status_created_at":
            col_name = col
            SQL_datatype = "DATE,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "retweeted_status_text":
            col_name = col
            SQL_datatype = "MEDIUMBLOB,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "retweeted_status_user_id":
            col_name = col
            SQL_datatype = "BIGINT,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "retweeted_status_username":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "retweeted_status_lang":
            col_name = col
            SQL_datatype = "TINYTEXT,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "retweeted_status_username_links":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "retweeted_status_username_friends_count":
            col_name = col
            SQL_datatype = "int,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "retweeted_status_username_followers_count":
            col_name = col
            SQL_datatype = "int,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "retweeted_status_username_listed_count":
            col_name = col
            SQL_datatype = "int,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "retweeted_status_username_status_count":
            col_name = col
            SQL_datatype = "int,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "retweeted_status_username_verified":
            col_name = col
            SQL_datatype = "TINYTEXT,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "retweeted_status_username_time_zone":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "retweeted_status_location":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "retweeted_status_location_coordinates":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "retweeted_status_hashtags":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "retweeted_status_user_mentions":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "retweeted_status_url":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "quoted_status":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "quoted_status_id":
            col_name = col
            SQL_datatype = "BIGINT,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "quoted_status_created_at":
            col_name = col
            SQL_datatype = "DATE,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "quoted_status_text":
            col_name = col
            SQL_datatype = "MEDIUMBLOB,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "quoted_status_user_id":
            col_name = col
            SQL_datatype = "BIGINT,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "quoted_status_username":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "quoted_status_lang":
            col_name = col
            SQL_datatype = "TINYTEXT,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "quoted_status_username_links":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "quoted_status_username_friends_count":
            col_name = col
            SQL_datatype = "int,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "quoted_status_username_followers_count":
            col_name = col
            SQL_datatype = "int,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "quoted_status_username_listed_count":
            col_name = col
            SQL_datatype = "int,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "quoted_status_username_status_count":
            col_name = col
            SQL_datatype = "int,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "quoted_status_username_verified":
            col_name = col
            SQL_datatype = "TINYTEXT,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "quoted_status_username_time_zone":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "quoted_status_location":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "quoted_status_location_coordinates":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "quoted_status_hashtags":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "quoted_status_user_mentions":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        elif col == "quoted_status_url":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "

        ## for sentiment analysis columns
        elif col == "tweet_length":
            col_name = col
            SQL_datatype = "int,"
            col_command = col_name + " " + SQL_datatype + " "

        elif col == "vader_tweet_pos":
            col_name = col
            SQL_datatype = "DOUBLE,"
            col_command = col_name + " " + SQL_datatype + " "

        elif col == "vader_tweet_neg":
            col_name = col
            SQL_datatype = "DOUBLE,"
            col_command = col_name + " " + SQL_datatype + " "

        elif col == "vader_tweet_compound":
            col_name = col
            SQL_datatype = "DOUBLE,"
            col_command = col_name + " " + SQL_datatype + " "

        elif col == "vader_tweet_neu":
            col_name = col
            SQL_datatype = "DOUBLE,"
            col_command = col_name + " " + SQL_datatype + " "

        elif col == "vader_tweet_category":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "

        elif col == "vader_tweet_sent_dict":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "

        elif col == "vader_tweet_sent_dict":
            col_name = col
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "

        else:
            print("The column name  '" + col + "' is not part of the regular list of variables and needs to be added manually")
        string_col_commands = string_col_commands + col_command
        sql_command = build_command + string_col_commands + ");"
    return(sql_command)


def pipe_remover(df):
    for col in df:
        col_name = col
        pandas_datatype = str(df[col].infer_objects().dtypes)
        print(col)
        print(pandas_datatype)
        if pandas_datatype == "string" and col !="tweet_id":
            print("TRUE")
            df[col_name] = df[col_name].str.replace("|", "")
            df[col_name] = df[col_name].str.replace('"', "")
            df[col_name] = df[col_name].str.replace("\n", "")
            df[col_name] = df[col_name].str.replace("\r", "")
        print(df.columns+ " pipe_remover")
    return df


def csv_to_SQL_formatter(in_filename, file_location, out_filename, db_table_name):
    df = csv_reader(in_filename, file_location) # read file
    df = indexer(df)
    df = pipe_remover(df)
    print(df.columns)
    sql_command = command_builder(df,db_table_name)
    current_path = os.getcwd()
    relative_file_path = os.path.join(current_path, file_location, out_filename)
    df.to_csv(relative_file_path, header=True, index=False, sep='|', mode='a')
    print(df.columns)
    print(sql_command)
    return(sql_command)

# Calling function

csv_to_SQL_formatter(in_filename, file_location, out_filename, db_table_name)
