import pandas as pd
import datetime
from subprocess import Popen
import os
import glob
import time
from sqlalchemy import create_engine

# convert the text files to powershell scripts

def DiomedesDB():
	'''MySQL database connection'''
	cnx = create_engine('bXlzcWwrcHlteXNxbDovL3VzZXJuYW1lOlBhc3N3b3JkQElQQWRkcmVzczozMzA2L0RhdGFiYXNl\nTmFtZQ==\n'.decode('base64','strict'), echo=False)
        return cnx


# Get current system date
d = datetime.datetime.now()
date = d.strftime("%m-%d-%y")


#Create a list to hold process handles
process_handles = []

#################################### User listing

#Run User list
process_handles.append(Popen(["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",".\DiomedesUsers"]))

############################# Groups

# cd to directory
os.chdir("/Diomedes/DomainGroups")


#Run domain 1
process_handles.append(Popen(["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",".\Domain1Groups"]))

#Run domain 2, etc.

################################## All Groups - no sub Groups

#Run domain 1
process_handles.append(Popen(["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",".\Domain1NonRecursiveGroups"]))

#Run domain 2, etc.

#Wait for all subprocesses to complete
for p in process_handles:
    p.wait()

################################## Process user files
filenamePath = 'Data/DiomedesUser_%s.csv' % date
DailyADUsers = pd.read_csv(filenamePath, skiprows = 1)

# Fill all NA values with zeros
DailyADUsers.fillna(0,inplace=True)

# Assign current date to Dataframe
DailyADUsers['RunDate'] = date

# Remove duplicate entries, if they exist
DailyADUsers.drop_duplicates(inplace=True)

################################## Combine group files
# Import all groups files
path = 'Data/'
location = path + 'DiomedesGroups*_%s.csv' % date
allFiles = glob.glob(location)
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_)
    list_.append(df)
frame = pd.concat(list_)

# Fill all NA values with zeros
DailyADGroups=frame.fillna(0)

# Change column name
DailyADGroups=DailyADGroups.rename(columns = {'Group Name':'Group_Name'})

# Assign current date to Dataframe
DailyADGroups['RunDate'] = date

# Remove duplicate entries, if they exist
DailyADGroups.drop_duplicates(inplace=True)

# Import all NonRecursive group files
pathNonRecursive = 'Data/'
locationNonRecursive = pathNonRecursive + 'DiomedesNonRecursiveGroups*_%s.csv' % date
allFilesNonRecursive = glob.glob(locationNonRecursive)
frameNonRecursive = pd.DataFrame()
list_NonRecursive = []
for file_NonRecursive in allFilesNonRecursive:
    dfNonRecursive = pd.read_csv(file_NonRecursive)
    list_NonRecursive.append(dfNonRecursive)
frameNonRecursive = pd.concat(list_NonRecursive)

# Fill all NA values with zeros

DailyADNonRecursiveGroups=frameNonRecursive.fillna(0)

# Change column name
DailyADNonRecursiveGroups=DailyADNonRecursiveGroups.rename(columns = {'Group Name':'Group_Name'})

# Assign current date to Dataframe
DailyADNonRecursiveGroups['RunDate'] = date

# Remove duplicate entries, if they exist
DailyADNonRecursiveGroups.drop_duplicates(inplace=True)
################################## Connect to Database

# Connect to Database
cnx = Diomedes()

DailyADUsers.to_sql("Users",con=cnx,if_exists='append', index=False)

DailyADGroups.to_sql("Groups",con=cnx,if_exists='append', index=False)

DailyADNonRecursiveGroups.to_sql("GroupsNonRecursive",con=cnx, if_exists='append', index=False)

############################
# Purge items from directory > 7 days old

def purgeDir(dir, age):
    """Small script (http://blog.rackspacecloudreview.com/86-freebie-python-chron-to-delete-files-older-than-x/)
    that scans a directory and deletes all files older than a specific
    date. It uses seconds, 86400 equals a day, so the last three days would be:
    (3*86400)"""
    print "Scanning:", dir
    for f in os.listdir(dir):
        now = time.time()
        filepath = os.path.join(dir, f)
        modified = os.stat(filepath).st_mtime
        if modified < now - age:
            if os.path.isfile(filepath):
                os.remove(filepath)
                print 'Deleted: %s (%s)' % (f, modified)

#Remove files that are over 2 days old.
purgeDir("Data/",(2*86400))


# Create success log file and post to log table
CurrentDate = datetime.datetime.now().strftime("%Y-%m-%d")
DictionaryTransformation = {'DateRan': CurrentDate,
                            'Group': 'DailyDiomedes',
                            'Status' : 'SUCCESS'}

Log = pd.DataFrame(DictionaryTransformation, index=[1])

Log.to_sql("DiomedesLog",con=cnx,if_exists='append', index=False)
