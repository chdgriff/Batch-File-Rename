import os
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

  def run(self):
    if not self.check_vars(): return self.error_msg
    self.find_and_replace()
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
    files_renamed = 0
    
    self.log.append("Directory: \""+fileDir+"\"\n")

    index = 0
    for file_name in os.listdir(fileDir):
      if self.file_count and index >= self.file_count: break
      if file_name in ignoredFiles: continue

      found_idx = file_name.find(self.find_text)
      if found_idx == -1: continue

      nextChar = found_idx + len(self.find_text) + self.offset # Finds the next character after text
  
      if nextChar >= len(file_name):   # If text found at the end of the filename
        new_name = file_name[:found_idx] + self.replace_text
      else:
        new_name = file_name[:found_idx] + self.replace_text + file_name[nextChar:]

      if not self.debug:
        os.rename(fileDir+"/"+file_name, fileDir+"/"+new_name)
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
      # if self.debug:

      self.log.append("\n" + str(files_renamed) + (" files" if files_renamed>1 else " file")+(" to be" if self.debug else '') + " renamed")
      # else:
      #   self.log.append(str(files_renamed) + " files" if file_renamed>0 else + " renamed")
    self.log.append("=====================================================================================\n")

  def stringify_log(self):
    log_string = ""
    return '\n'.join(self.log)

