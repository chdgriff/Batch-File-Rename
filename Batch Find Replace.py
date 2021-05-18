import os
from os import path
import string
import sys, getopt

# This is a python script to find and replace file names in a
# given directory.

DIRECTORY       = "E:\\Anime\\Tokyo Ghoul\\Season 3"
FIND            = "S02"
#
#
REPLACE         = "S03"
#

NUM_START       = 1
NUM_END         = 0          # inclusive
#65
DEBUG           = True          # Change default behavior
SEASONS         = False
SEASON_START    = 1
SEASON_END       = 18              # Not inclusive

def batchFileFindandReplace(s=""):
    fileDir = DIRECTORY + s
    filesRenamed = 0

    if not os.path.isdir(fileDir):
        print("ERROR: \""+fileDir+"\" cannot be found")
        exit()
    print("\nDirectory: \""+fileDir+"\"\n")

    index = NUM_START
    for fileName in os.listdir(fileDir):
        if NUM_END and index > NUM_END:
            break
        foundIndex = fileName.find(FIND)
        if foundIndex == -1:                 # If not found
            continue;

        nextChar = foundIndex + len(FIND)# Finds the next character after FIND
        #REPLACE = "One Piece S"+s+"E"
        if nextChar >= len(fileName):   # If found at the end of the name
            newName = fileName[:foundIndex] + REPLACE
        else:
            newName = fileName[:foundIndex] + REPLACE + fileName[nextChar:]

        if not DEBUG:
            os.rename(fileDir+"/"+fileName, fileDir+"/"+newName)
        print(fileName + " --> " + newName)
        filesRenamed += 1
        index += 1
    return filesRenamed

def introMessage(s=""):
    print("\n================================================================================")
    print("             Starting Batch File Name Find and Replace")
    print("================================================================================")


def endingMessage(filesRenamed=0):
    print()
    if filesRenamed == 0:
        print("No files found with \""+FIND+"\" Did you mean something else?")
    else:
        if DEBUG:
            print(str(filesRenamed) + " files to be renamed")
        else:
            print(str(filesRenamed) + " files renamed")

def default():
    filesRenamed = batchFileFindandReplace()
    endingMessage(filesRenamed)
    print("================================================================================\n")

def seasons():
    totalFilesRenamed = 0
    for num in range(SEASON_START, SEASON_END):
        if SEASON_END-1 > 9:
            season = str(num).zfill(2)
        else:
            season = str(num)
        filesRenamed = batchFileFindandReplace(season)
        endingMessage(filesRenamed)
        print("\n")
        totalFilesRenamed += filesRenamed
    print(str(totalFilesRenamed)+" files renamed in total")
    print("================================================================================\n")

def main():
    opts, args = getopt.getopt(sys.argv[1:], "wt")
    for opt, arg in opts:
        if opt == '-w':
            global DEBUG
            DEBUG = False
    introMessage()
    if not DEBUG:
        print("Confirm Rename")
        input()
    if SEASONS:
        seasons()
    else:
        default()


if __name__ == "__main__":
    main()
