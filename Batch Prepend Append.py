import os
import string
import sys, getopt

# This is a python script to find and replace file names in a
# given directory.

DIRECTORY       = "D:\\TV Shows\\One Piece"

TEXT                = ""          # text to be added (not enumerated)
NUM                 = True        # enumerate text added
PREPEND_OR_APPEND   = 'P'               # [A, P] Defaults to Prepend

# Text around number to be added
NUM_L               = "One Piece S21E"          # text {number}
NUM_R               = ""                           # {number} text


DIGITS              = 3                 # Number of digits for the number to add e.g. 001 vs 1

# Number of files to be renamed
NUM_START           = 1
NUM_END             = 0                 # inclusive (0 means for all files)

DEBUG               = True              # change default behavior from requiring '-w' to write filenames

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

def main():
    opts, args = getopt.getopt(sys.argv[1:], "wt")
    for opt, arg in opts:
        if opt == '-w':
            global DEBUG
            DEBUG = False
    introMessage()
    default()


if __name__ == "__main__":
    main()
