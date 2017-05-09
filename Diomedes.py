# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 15:37:07 2017

@author: aclark
"""


import pandas as pd
import sqlite3
import datetime
from subprocess import check_call
import os
import glob
import time


# Get current system date
d = datetime.datetime.now()
date = d.strftime("%m-%d-%y")

#################################### User listing

# cd to directory
os.chdir("repos/Diomedes")


#Run User list
check_call(["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",".\DiomedesUsers"])

filenamePath = 'Diomedes/data/DiomedesUser_%s.csv' % date
DailyADUsers = pd.read_csv(filenamePath, skiprows = 1)

# Fill all NA values with zeros
DailyADUsers.fillna(0,inplace=True)

# Assign current date to dataframe
DailyADUsers['RunDate'] = date

# Remove duplicate entries, if they exist
DailyADUsers.drop_duplicates(inplace=True)
############################# Groups

# cd to directory
os.chdir("/Diomedes/DomainGroups")


#Run domain 1
check_call(["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe","./Domain1Groups"])

#Run domain 2, etc.

# Import all groups files
path = '/Diomedes/data/'
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

# Assign current date to dataframe
DailyADGroups['RunDate'] = date

# Remove duplicate entries, if they exist
DailyADGroups.drop_duplicates(inplace=True)
################################## All Groups - no sub Groups

# cd to directory
os.chdir("/Diomedes/DomainGroupsNoSubGroups")

#Run domain 1
check_call(["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe","./Domain1NonRecursiveGroups"])

#Run domain 2, etc.

# Import all NonRecursive group files
pathNonRecursive = '/Diomedes/data/'
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

# Assign current date to dataframe
DailyADNonRecursiveGroups['RunDate'] = date

# Remove duplicate entries, if they exist
DailyADNonRecursiveGroups.drop_duplicates(inplace=True)
################################## Connect to database
# Connect to SQLite database
SQL3conn = sqlite3.connect('/Diomedes.db')

DailyADUsers.to_sql("Users",con=SQL3conn,if_exists='append')

DailyADGroups.to_sql("Groups",con=SQL3conn,if_exists='append')

DailyADNonRecursiveGroups.to_sql("GroupsNonRecursive",con=SQL3conn,if_exists='append')

SQL3conn.close()

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

#Remove files that are over 7 days old.
purgeDir("/Diomedes/data/",(7*86400))
