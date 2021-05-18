import os
import string
import sys, getopt

# This is a python script to find and replace file names in a
# given directory.

DIRECTORY       = "D:\\TV Shows\\One Piece"
TEXT                = ""
NUM                 = True        # enumerate
NUM_L               = "One Piece S21E"          # text {number}
NUM_R               = ""                           # {number} text
DIGITS              = 3
PREPEND_OR_APPEND   = 'P'               # [A, P] Defaults to Prepend
NUM_START           = 53
NUM_END             = 107                 # inclusive

DEBUG               = True

SEASONS             = False
SEASON_START        = 1
SEASON_END           = 18              # Not inclusive


def batchPrependAppend(s=""):
    fileDir = DIRECTORY + s
    filesRenamed = 0
    if DEBUG:
        print("--------------------------------DEBUG--------------------------------")
    print("\nDirectory: \""+fileDir+"\"\n")
    index = NUM_START
    for fileName in os.listdir(fileDir):
        if NUM_END and index > NUM_END:
            break

        if NUM:
            textToAdd = NUM_L+str(index).zfill(DIGITS)+NUM_R
            #print(textToAdd)
        else:
            textToAdd = TEXT

        if PREPEND_OR_APPEND == 'A':
            newName = os.path.splitext(fileName)[0]+textToAdd+os.path.splitext(fileName)[1]
        else:
            newName = textToAdd+fileName

        if not DEBUG:
            os.rename(fileDir+"/"+fileName, fileDir+"/"+newName)
        print(fileName + " --> " + newName)
        filesRenamed += 1
        index += 1
    return filesRenamed

def introMessage(s=""):
    print("=====================================================================")
    print("             Starting Batch File Prepend or Append")
    print("=====================================================================")


def endingMessage(filesRenamed=0):
    print()
    if filesRenamed == 0:
        print("No files found with \""+FIND+"\" Did you mean something else?\n")
    else:
        if DEBUG:
            print(str(filesRenamed) + " files to be renamed")
        else:
            print(str(filesRenamed) + " files renamed")

def default():
    filesRenamed = batchPrependAppend()
    endingMessage(filesRenamed)
    print("=====================================================================\n")

def seasons():
    totalFilesRenamed = 0
    for num in range(SEASON_START, SEASON_END):
        if SEASON_END-1 > 9:
            season = str(num).zfill(2)
        else:
            season = str(num)
        introMessage(season)
        filesRenamed = batchPrependAppend(season)
        endingMessage(filesRenamed)
        print("\n")
        totalFilesRenamed += filesRenamed
    print(str(totalFilesRenamed)+" files renamed in total")
    print("=====================================================================\n")

def main():
    opts, args = getopt.getopt(sys.argv[1:], "wt")
    for opt, arg in opts:
        if opt == '-w':
            global DEBUG
            DEBUG = False
    introMessage()
    if SEASONS:
        seasons()
    else:
        default()


if __name__ == "__main__":
    main()
