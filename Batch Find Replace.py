import os, string, sys, getopt
from tkinter import filedialog
from Ignored_Files import fileList as ignoredFiles

class BatchFindReplace():
  def __init__(self, file_path, find_text, offset, replace_text, file_count, debug=True):
    self.file_path = file_path
    self.find_text = find_text
    self.offset = offset
    self.replace_text = replace_text
    self.file_count = file_count
    self.debug = debug
    self.log = []

    self.error_msg = ""

    if not self.check_vars(): return self.error_msg
    files_renamed = self.find_and_replace()
    self.end_message(files_renamed)
    return self.stringify_log()

  # Checks variables for valid values
  def check_vars(self):
    if not os.path.isdir(self.file_path):
      self.error_msg = "ERROR: \""+self.file_path+"\" cannot be found"
      return False
    if self.offset < 0:
      self.error_msg = "ERROR: offset cannot be less than zero"
      return False
    if self.file_count < 0:
      self.error_msg = "ERROR: file count must be 0 or greater"
      return False
    return True

  # main function that runs the overall find and replace function.
  def find_and_replace(self, n=""):
    self.intro_message()
    fileDir = self.file_path + n
    filesRenamed = 0
    
    self.log.append("\nDirectory: \""+fileDir+"\"\n")

    index = 0
    for fileName in os.listdir(fileDir):
      if self.file_count and index >= self.file_count: break
      if fileName in ignoredFiles: continue

      foundIndex = fileName.find(self.find_text)
      if foundIndex == -1:continue

      nextChar = foundIndex + len(self.find_text) + self.offset # Finds the next character after text
  
      if nextChar >= len(fileName):   # If text found at the end of the filename
        newName = fileName[:foundIndex] + self.replace_text
      else:
        newName = fileName[:foundIndex] + self.replace_text + fileName[nextChar:]

      if not self.debug:
        os.rename(fileDir+"/"+fileName, fileDir+"/"+newName)
      print(fileName + " --> " + newName)
      filesRenamed += 1
      index += 1
    self.end_message(filesRenamed)

  def intro_message(self):
    self.log.append("======================================================================================")
    self.log.append("                    Starting Batch File Name Find and Replace")
    self.log.append("======================================================================================")
  

  def end_message(self, filesRenamed=0):
    self.log.append("\n")
    if filesRenamed == 0:
      self.log.append("No files found with \""+self.find_text+"\" Did you mean something else?")
    else:
      if self.debug:
        self.log.append(str(filesRenamed) + " files to be renamed")
      else:
        self.log.append(str(filesRenamed) + " files renamed")
    self.log.append("======================================================================================\n")

  def stringify_log(self):
    log_string = ""
    return '\n'.join(self.log)

