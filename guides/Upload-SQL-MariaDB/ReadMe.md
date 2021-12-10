# Upload a file to SQL database

**This code demonstrates how to upload files into SQL.** The files should begin as a `.csv` file, typically from a dataframe.

Useful rescources with more detail: 

https://grid.rcs.hbs.org/importing

https://grid.rcs.hbs.org/import-and-export-text-files

**A. Format File** - prepare the file for upload into SQL database by changing its format into a pipe-separated (`|`) `.txt` file
1. Open csv-to-txt-for-SQL.py
2. Change in_filename, out_filename, db_table_name, file_location in lines 6 - 9 to your specific files and directories
3. Run the code. The code will output A. formatted txt-file and B. a command which can be used to create the sql-table
4. Copy the command so you enter it in for step 3. of the Create Database process below
5. Move the txt file onto the GRID's desktop for the Move File process below

**B. Create Database** - enter the GRID (or SecureCRT) and use the following commands on the command line interface.
1. `mysql`
2. `use agoldenberg_twitter_data;`
3. `create table table_import (Column_1 char(20), Column_2 char(20), Column_3 char(20));` - this command should have also appeared in the file formatter above

**Create Import Directory**
1. `mkdir /export/mdb_external/import/username`
2. `chmod 700 /export/mdb_external/import/username`

**Move File**
1. `pwd` #Get the full directory of your desktop where your file is
returns for example: `/export/home/rcsguest/rcs_username/Desktop`
2. `mv /export/home/rcsguest/rcs_username/Desktop/SampleData.txt /export/mdb_external/import/username`

**Import File**
1. `mysql`
2. `use agoldenberg_DATABASENAME;`
3. `load data local infile '/export/mdb_external/import/username/SampleData.txt' into table table_import fields terminated by '|' lines terminated by '\n' ignore 1 lines;`

**Check Data**
1. `Describe TABLENAME;`
2. `SELECT * FROM TABLENAME;`

**Remove temp-import files & folder**
1. rm -rf /export/mdb_external/import/username

