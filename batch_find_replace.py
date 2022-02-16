import os
from Ignored_Files import file_list as ignored_files
from core import *

class BatchFindReplace(BatchFileNameOperations):
  def __init__(self, file_path, find_text, offset, replace_text, ignore_case, file_count, debug=True):
    super().__init__(file_path, file_count, debug)
    self.find_text = find_text
    self.offset = offset
    self.replace_text = replace_text
    self.ignore_case = ignore_case
    self.find_text = find_text.upper() if self.ignore_case else find_text

    self.error_msg = ""

  def run(self):
    if not self.check_vars(): return self.error_msg
    self.find_and_replace()
    return super().stringify_log()

  # Checks variables for valid values
  def check_vars(self):
    if not super().check_core_vars(): return False
    if self.offset < 0:
      self.error_msg = "ERROR: offset cannot be less than zero"
      return False
    return True

  # main function that runs the overall find and replace function.
  def find_and_replace(self, n=""):
    self.intro_message()
    file_directory = self.file_path + n
    files_renamed = 0
    
    self.log.append("Directory: \""+file_directory+"\"\n")

    index = 0
    for file_name in os.listdir(file_directory):
      if self.file_count and index >= self.file_count: break
      if file_name in ignored_files: continue

      found_idx = (file_name.upper() if self.ignore_case else file_name).find(self.find_text)
      if found_idx == -1: continue


      file_extension_idx = file_name.rfind('.')
      nextChar = found_idx + len(self.find_text) + self.offset # Finds the next character after text
      if nextChar > file_extension_idx: nextChar = file_extension_idx
      
  
      if nextChar >= len(file_name):   # If text found at the end of the filename
        new_name = file_name[:found_idx] + self.replace_text
      else:
        new_name = file_name[:found_idx] + self.replace_text + file_name[nextChar:]

      if not self.debug:
        os.rename(file_directory+"/"+file_name, file_directory+"/"+new_name)
      self.log.append(file_name + " --> " + new_name)
      files_renamed += 1
      index += 1
    self.end_message(files_renamed)

  def intro_message(self):
    self.log.append("\n=====================================================================================")
    self.log.append("{:^90s}".format("Starting Batch File Name Find and Replace"))
    self.log.append("=====================================================================================")
  

  def end_message(self, files_renamed=0):
    if files_renamed == 0:
      self.log.append("\nNo files found with \""+self.find_text+"\" Did you mean something else?")
    else:
      self.log.append("\n" + str(files_renamed) + (" files" if files_renamed>1 else " file")+(" to be" if self.debug else '') + " renamed")
    self.log.append("=====================================================================================\n")

