import os
from os import path
import string
import sys, getopt

# This is a python script to find and replace file names in a
# given directory.

DIRECTORY       = "E:\Downloads\Its.Always.Sunny.In.Philadelphia.S13.1080p.AMZN.WEBRip.DDP5.1.x264-NTb[rartv]"   
FIND            = "[Judas] Highschool of the Dead - "
REPLACE         = "Highschool of the Dead S01E"
REMOVE_PERIODS  = True

# number of files to be renamed
NUM_START       = 1
NUM_END         = 0          # inclusive

DEBUG           = True          # Default behavior requiring "-w" flag to write filenames

# If recuring through numbered directories e.g. folder1, folder2, folder3
NUM_DIR         = False
NUM_START       = 1
NUM_END         = 18              # Inclusive

def fixPath(path):
  newPath = ''
  for c in path:
    if c == '\\':
      newPath += '\\\\'
    else:
      newPath += c
  return newPath

def checkDirectory(path):
  if not os.path.isdir(path):
    print("ERROR: \""+path+"\" cannot be found")
    exit()
  return True

def batchFileFindandReplace(n=""):
  fileDir = DIRECTORY + n
  filesRenamed = 0
  checkDirectory(fileDir)
  
  print("\nDirectory: \""+fileDir+"\"\n")

  index = NUM_START
  for fileName in os.listdir(fileDir):
    if NUM_END and index > NUM_END:
      break
    foundIndex = fileName.find(FIND)
    if foundIndex == -1:                 # If not found
      continue

    nextChar = foundIndex + len(FIND)# Finds the next character after text
 
    if nextChar >= len(fileName):   # If text found at the end of the filename
      newName = fileName[:foundIndex] + REPLACE
    else:
      newName = fileName[:foundIndex] + REPLACE + fileName[nextChar:]

    if not DEBUG:
      os.rename(fileDir+"/"+fileName, fileDir+"/"+newName)
    print(fileName + " --> " + newName)
    filesRenamed += 1
    index += 1
  return filesRenamed

def introMessage():
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
  print("================================================================================\n")

def default():
  filesRenamed = batchFileFindandReplace()
  endingMessage(filesRenamed)
  

def numberedDirectory():
  totalFilesRenamed = 0
  for num in range(NUM_START, NUM_END+1):
    if NUM_END > 9:
      number = str(num).zfill(2)
    else:
      number = str(num)
    filesRenamed = batchFileFindandReplace(number)
    endingMessage(filesRenamed)
    print("\n")
    totalFilesRenamed += filesRenamed
  print(str(totalFilesRenamed)+" files renamed in total")
  print("================================================================================\n")

def removePeriods():
  filesRenamed = 0
  fileDir = DIRECTORY
  checkDirectory(fileDir)

  for fileName in os.listdir(fileDir):
    temp = fileName.split('.')
    newName = ' '.join(temp[:-1]) + '.' + temp[-1]
	
    if not DEBUG:
      os.rename(fileDir+"/"+fileName, fileDir+"/"+newName)
    print(fileName + " --> " + newName)
    filesRenamed += 1
  endingMessage(filesRenamed)


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
  if NUM_DIR:
    numberedDirectory()
  elif REMOVE_PERIODS:
    removePeriods()
  else:
    default()


if __name__ == "__main__":
  main()
