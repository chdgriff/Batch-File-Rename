import os, string, sys, getopt

# This is a python script to find and replace file names in a
# given directory.

# ./Batch Find Replace.py             Test program and see filenames to be updated
# ./Batch Find Replace.py -w          Write out and replace filenames
# To use input the correct directory and options within the macros below.

DIRECTORY       = "D:\Anime\Baki The Grappler\Season 01"        # Make sure to properly escape \N or \t to \\N and \\t respectively
FIND            = "Baki The Grappler "
OFFSET          = 0                                            # Additonal characters to find and replace
REPLACE         = "Baki the Grappler "

# In case where file name is divided by tokens i.e a.file.name.pdf or a_file_name.pdf
REMOVE_TOKENS   = False                   # Changing to true only removes tokens not find and replace.
TOKEN           = '_'

FILE_COUNT      = 0             # Default is 0 for all files found. 

DEBUG           = True          # Default behavior requires "-w" flag to write filenames. Change to false to always write file names

# If recuring through numbered directories e.g. folder01, folder02, folder03
# Change NUM_START and NUM_END
NUM_DIR         = False
NUM_SIZE        = 2             # Change digit count for numbers i.e. 01 vs 001 vs 1
NUM_START       = 1             
NUM_END         = 0             # inclusive, 0 for all folders

def fixPath(path):
  newPath = ''
  for c in path:
    if c == '\\':
      newPath += '\\\\'
    else:
      newPath += c
  return newPath

# Checks if directory at path exists
def checkDirectory(path):
  if not os.path.isdir(path):
    print("ERROR: \""+path+"\" cannot be found")
    exit()
  return True

# Checks Macros for valid values
def checkUserMacros():
  checkDirectory(DIRECTORY)
  if OFFSET < 0:
    print("ERROR: OFFSET cannot be less than zero\n")
    exit()
  if FILE_COUNT < 0:
    print("ERROR: FILE_COUNT must be 0 or greater")
    exit()
  if NUM_START < 0:
    print("ERROR: NUM_START must be 0 or greater")
    exit()
  if NUM_END < 0:
    print("ERROR: NUM_END must be 0 or greater")
    exit()
  if OFFSET < 0:
    print("ERROR: OFFSET cannot be less than zero\n")
    exit()
  return True

# Checks for correct command line arguments
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

# main function that runs the overall find and replace function.
def batchFileFindandReplace(n=""):
  introMessage()
  fileDir = DIRECTORY + n
  filesRenamed = 0
  checkDirectory(fileDir)
  
  print("\nDirectory: \""+fileDir+"\"\n")

  index = 0
  for fileName in os.listdir(fileDir):
    if FILE_COUNT and index >= FILE_COUNT:
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

def removeToken(token = '.'):
  introMessage("token")
  filesRenamed = 0
  fileDir = DIRECTORY

  index = NUM_START
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
    index += 1
  return filesRenamed

def introMessage(opt="default"):
  print("\n======================================================================================")
  
  if opt == "token":
    print("             Starting Batch Token Remover")
  elif opt == "default":
    print("             Starting Batch File Name Find and Replace")
  print("======================================================================================")
  

def endingMessage(filesRenamed=0):
  print()
  if filesRenamed == 0:
    print("No files found with \""+FIND+"\" Did you mean something else?")
  else:
    if DEBUG:
      print(str(filesRenamed) + " files to be renamed")
    else:
      print(str(filesRenamed) + " files renamed")
  print("======================================================================================\n")

def numberedDirectory():
  totalFilesRenamed = 0
  for num in range(NUM_START, NUM_END+1):
    number = str(num).zfill(NUM_SIZE)
    filesRenamed = batchFileFindandReplace(number)
    endingMessage(filesRenamed)
    print("\n")
    totalFilesRenamed += filesRenamed
  print(str(totalFilesRenamed)+" files renamed in total")
  print("===================================================================================\n")

def main():
  getArgs()
  checkUserMacros()

  if not DEBUG:
    print("Confirm Rename")
    input()
  if NUM_DIR:
    numberedDirectory()
  else:
    if REMOVE_TOKENS:
      filesRenamed = removeToken(TOKEN)
    else:
      filesRenamed = batchFileFindandReplace()
    endingMessage(filesRenamed)

if __name__ == "__main__":
  main()
