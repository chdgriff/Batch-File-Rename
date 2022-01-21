import os
from core import *
from Ignored_Files import file_list as ignored_files

class BatchRemoveTokens(BatchFileNameOperations):
  def __init__(self, file_path, file_count, token, debug) -> None:
    super().__init__(file_path, file_count, debug)
    self.token = token

  def run(self):
    if not self.check_vars(): return self.error_msg
    self.removeTokens()
    super().stringify_log

  def check_vars(self):
    if not super().check_core_vars(): return False
    return True

  def removeTokens(self):
    self.intro_message()
    files_renamed = 0

    index = 0
    for file_name in os.listdir(self.file_path):
      if file_name in ignored_files: continue
      if self.file_count and index >= self.file_count: break
      
      temp = file_name.split(self.token)
      if self.token == '.':
        new_name = ' '.join(temp[:-1]) + '.' + temp[-1]
      else:
        new_name = ' '.join(temp)

      if not self.debug:
        os.rename(self.file_path+"/"+file_name, self.file_path+"/"+new_name)
      self.log.append(file_name + " --> " + new_name)
      files_renamed += 1
      index += 1
    self.end_message(files_renamed)

  def intro_message(self):
    self.log.append("\n=====================================================================================")
    self.log.append("{:^90s}".format("Starting Batch File Token Remover"))
    self.log.append("=====================================================================================")
  
  def end_message(self, files_renamed=0):
    if files_renamed == 0:
      self.log.append("\nNo files found with token:\'"+self.token+"\' Did you mean something else?")
    else:
      self.log.append("\n" + str(files_renamed) + (" files" if files_renamed>1 else " file")+(" to be" if self.debug else '') + " renamed")
    self.log.append("=====================================================================================\n")
  