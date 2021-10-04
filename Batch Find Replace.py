import os
from os import path
import string
import sys, getopt

# This is a python script to find and replace file names in a
# given directory.

DIRECTORY       = "D:\Anime\Baki The Grappler\Season 01"
FIND            = "Baki The Grappler "
REPLACE         = "Baki the Grappler "
REMOVE_TOKENS   = False
TOKEN           = '_'

OFFSET          = 0          # Additonal characters to replace

# number of files to be renamed
NUM_START       = 1
NUM_END         = 0          # inclusive

DEBUG           = True          # Default behavior requiring "-w" flag to write filenames

# If recuring through numbered directories e.g. folder1, folder2, folder3
NUM_DIR         = False

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

def getArgs():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "wt")
  except getopt.GetoptError as err:
    print("ERROR: " + str(err.args[0])+'\n\n')
    exit()
  for opt, arg in opts:
    if opt == '-w':
      global DEBUG
      DEBUG = False

def batchFileFindandReplace(n=""):
  introMessage()
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

    nextChar = foundIndex + len(FIND) + OFFSET # Finds the next character after text
 
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

def baki(n=""):
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
    nextChar = foundIndex + len(FIND) + 10
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



  

def introMessage(opt="default"):
  print("\n================================================================================")
  
  if opt == "token":
    print("             Starting Batch Token Remover")
  elif opt == "default":
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

def removeToken(token = '.'):
  introMessage("token")
  filesRenamed = 0
  fileDir = DIRECTORY
  checkDirectory(fileDir)

  for fileName in os.listdir(fileDir):
    temp = fileName.split(token)
    if token == '.':
      newName = ' '.join(temp[:-1]) + '.' + temp[-1]
    else:
      newName = ' '.join(temp)
	
    if not DEBUG:
      os.rename(fileDir+"/"+fileName, fileDir+"/"+newName)
    print(fileName + " --> " + newName)
    filesRenamed += 1
  endingMessage(filesRenamed)


def main():
  getArgs()
  global DIRECTORY
  #DIRECTORY = fixPath(DIRECTORY)
  if not DEBUG:
    print("Confirm Rename")
    input()
  if NUM_DIR:
    numberedDirectory()
  elif REMOVE_TOKENS:
    removeToken(TOKEN)
  else:
    default()


if __name__ == "__main__":
  main()
