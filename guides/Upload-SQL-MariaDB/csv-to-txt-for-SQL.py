import pandas as pd
import os

# Defining files and locations

in_filename = "twitter-hook-data" + ".csv"
file_location = "data"
out_filename = "twitter-hook-data-oct-21-sample" + ".txt"
db_table_name = "twitter-hook-data-oct-21"

# Functions

def csv_reader(in_filename, file_location):
    current_path = os.getcwd()
    relative_file_path = os.path.join(current_path, file_location, in_filename)
    df = pd.read_csv(relative_file_path,  # reading in the original dataset
                     error_bad_lines=False,
                     index_col=False)
    #df.update(df.select_dtypes(include=np.number).applymap('{:,g}'.format)) # remove trailing 0s
    df = df.convert_dtypes()
    return df

def indexer(df):
    df.reset_index(inplace=True, drop=True)
    filter_col = [col for col in df if not col.startswith('Unnam') and not col.startswith('X')] # remove unwanted columns
    df = df[filter_col]
    return df

def command_builder(df,db_table_name):
    build_command = "create table " + db_table_name + " ("
    string_col_commands = ""
    for col in df:
        col_name = col
        pandas_datatype = str(df[col].infer_objects().dtypes)
        #print(col,pandas_datatype)
        if pandas_datatype == "Int64":
            SQL_datatype = "int,"
            col_command = col_name + " " + SQL_datatype + " "
        elif pandas_datatype == "float64":
            df[col] = df[col].round(5)
            SQL_datatype = "decimal(18,5),"
            col_command = col_name + " " + SQL_datatype + " "
        elif pandas_datatype == "string":
            SQL_datatype = "text,"
            col_command = col_name + " " + SQL_datatype + " "
        else:
            print(col + " " + str(pandas_datatype) + " Jonas has not added this datatype yet")
        string_col_commands = string_col_commands + col_command
    sql_command = build_command + string_col_commands + ");"
    return(sql_command)

def pipe_remover(df):
    for col in df:
        col_name = col
        pandas_datatype = str(df[col].infer_objects().dtypes)
        if pandas_datatype == "string":
            df[col_name] = df[col_name].str.replace("|", "")
    return df


def csv_to_SQL_formatter(in_filename, file_location, out_filename, db_table_name):
    df = csv_reader(in_filename, file_location) # read file
    df = indexer(df)
    sql_command = command_builder(df,db_table_name)
    df = pipe_remover(df)
    current_path = os.getcwd()
    relative_file_path = os.path.join(current_path, file_location, out_filename)
    df.to_csv(relative_file_path, header=True, index=False, sep='|', mode='a')
    return(sql_command)

# Calling function

csv_to_SQL_formatter(in_filename, file_location, out_filename, db_table_name)
