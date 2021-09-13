Useful rescources with more detail: 
https://grid.rcs.hbs.org/importing
https://grid.rcs.hbs.org/import-and-export-text-files

Create Database
1. mysql
2. use agoldenberg_twitter_data;
3. create table table_import (Column_1 char(20), Column_2 char(20), Column_3 char(20));

Create Import Directory
1. mkdir /export/mdb_external/import/username
2. chmod 700 /export/mdb_external/import/username

Move File
1. pwd #Get the full directory of your desktop where your file is
returns for example: /export/home/rcsguest/rcs_username/Desktop
2. mv /export/home/rcsguest/rcs_username/Desktop/SampleData.txt /export/mdb_external/import/username

Import File
1. mysql
2. use agoldenberg_DATABASENAME;
3. load data local infile '/export/mdb_external/import/username/SampleData.txt' into table table_import fields terminated by '|' lines terminated by '\n' ignore 1 lines;

Check Data
1.Describe table_import;
2. SELECT * FROM table_import;

Remove temp-import files & folder
1. rm -rf /export/mdb_external/import/username

