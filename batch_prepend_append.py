import os
from Ignored_Files import file_list as ignored_files
from core import *

class BatchPrependAppend(BatchFileNameOperations):
  """
  Runs prepend or append on filenames in a givern directory
  

  --------
  Methods:
  --------
  run() -> str
    Runs overall operations
  check_vars() -> bool
    Error checks the attributes
  """

  def __init__(self, dir_path, text, prepend_append, file_count, debug):
    super().__init__(dir_path, file_count, debug)
    self.text = text
    self.prepend_append = prepend_append

  def run(self) -> str:
    """Runs overall operations."""
    if not self.check_vars(): return self.error_msg
    self._prepend_append_text()
    return super().stringify_log()
  
  def check_vars(self) -> bool:
    if not super().check_core_vars(): return False
    return True

  def _prepend_append_text(self):
    self._intro_message()
    files_renamed = 0
    file_dir = self.dir_path

    self.log.append("Directory: \"{file_dir}\"\n")
    index = 0
    for file_name in os.listdir(file_dir):
      if os.path.isdir(os.path.join(self.dir_path, file_name)): continue
      if file_name in ignored_files: continue
      if self.file_count and index >= self.file_count: break

      if self.prepend_append == 'A':
        new_name = os.path.splitext(file_name)[0]+self.text+os.path.splitext(file_name)[1]
      else:
        new_name = self.text+file_name

      if not self.debug: # Writes out new file name if not debug
        os.rename(os.path.join(self.dir_path,file_name), os.path.join(self.dir_path, new_name))
      self.log.append(file_name + " --> " + new_name)
      files_renamed += 1
      index += 1


    self._end_message(files_renamed)

  def _intro_message(self):
    self.log.append("\n=====================================================================================")
    self.log.append("{:^90s}".format("Starting Batch Prepend or Append"))
    self.log.append("=====================================================================================")

  def _end_message(self, files_renamed=0):
    if files_renamed == 0:
      self.log.append("\nNo files renamed, did you specify the wrong directory?")
    else:
      self.log.append(f"\n{files_renamed}{' Files' if files_renamed>1 else ' File'}{' To Be' if self.debug else ''} Renamed")
    self.log.append("=====================================================================================\n")