import os, string, sys, getopt

# This is a python script find and adjust numbers found 
# for filenames in a given directory.

DIRECTORY       = "E:\Anime\One Piece\Season 16"      # \n or \t must be properly escapped with '\\'

# Input piece of text to find with '##' for the placeholder of the numbers to replace.
# '##' must be at the end of the text to locate
FIND            = "One Piece S16E##"                  


ADJUST          = 578                                 # number to adjust the numbers by, can be negative

# Number of files to renamed
FILE_COUNT = 0         																# inclusive (0 means all files in given directory)

DEBUG           = True          # Change default behavior

# If recuring through numbered directories e.g. folder1, folder2, folder3
NUM_DIR         = False
NUM_START       = 1
NUM_END         = 18              # Inclusive

def batchNumAdjust(n=""):
  fileDir = DIRECTORY + n
  filesRenamed = 0

  if not os.path.isdir(fileDir):
    print("ERROR: \""+fileDir+"\" cannot be found")
    exit()
  print("\nDirectory: \""+fileDir+"\"\n")

  index = 0
  oldFINDGen = oldSubstring(FIND)
  newFINDGen = newSubstring(FIND)
  foundIndex = -1
  oldFIND = next(oldFINDGen)
  for fileName in os.listdir(fileDir):
    if FILE_COUNT and index >= FILE_COUNT:
      break
    if foundIndex != -1:
      oldFIND = next(oldFINDGen)
    # print(fileName)
    # print(oldFIND)
    foundIndex = fileName.find(oldFIND)
    if foundIndex == -1:                 # If not found
      continue

    nextChar = foundIndex + len(FIND)# Finds the next character after FIND
    newFIND = next(newFINDGen)

    if nextChar >= len(fileName):   # If found at the end of the name
      newName = fileName[:foundIndex] + newFIND
    else:
      newName = fileName[:foundIndex] + newFIND + fileName[nextChar:]

    if not DEBUG:
      os.rename(fileDir+"/"+fileName, fileDir+"/"+newName)
    print(fileName + " --> " + newName)
    filesRenamed += 1
    index += 1
  return filesRenamed

# Requires '#' to be at end of FIND
def findDigitCount(subString):
  digits = 0
  for i in range(len(subString)-1,-1,-1):
    if subString[i] == '#':
      digits += 1
    else:
      break
  return digits

def oldSubstring(startFileName: str)-> str:
  digits = findDigitCount(startFileName)
  i = NUM_START
  while True:
    yield startFileName[:len(startFileName)-digits]+str(i).zfill(digits)
    i+=1

def newSubstring(startFileName: str)-> str:
  digits = findDigitCount(startFileName)
  i = NUM_START
  while True:
    yield startFileName[:len(startFileName)-digits]+str(i).zfill(digits)+" "+str(i+ADJUST)
    i+=1

def introMessage(s=""):
  print("\n======================================================================================")
  print("                Starting Batch File Name Find and Replace")
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

def default():
  filesRenamed = batchNumAdjust()
  endingMessage(filesRenamed)
  print("======================================================================================\n")

def numberedDirectory():
  totalFilesRenamed = 0
  for num in range(NUM_START, NUM_END+1):
    if NUM_END > 9:
      number = str(num).zfill(2)
    else:
      number = str(num)
    filesRenamed = batchNumAdjust(number)
    endingMessage(filesRenamed)
    print("\n")
    totalFilesRenamed += filesRenamed
  print(str(totalFilesRenamed)+" files renamed in total")
  print("======================================================================================\n")

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
  else:
    default()


if __name__ == "__main__":
  main()
