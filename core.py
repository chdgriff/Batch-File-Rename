import os

class BatchFileOperations():
  def __init__(self, file_path, file_count, debug=True) -> None:
      self.file_path = file_path
      self.file_count = file_count
      self.debug = debug
      self.log = []
      self.error_msg = ""
  
  def check_core_vars(self):
    if not self.check_file_path():
      self.error_msg = "ERROR: \""+self.file_path+"\" cannot be found"
      return False
    if self.file_count < 0:
      self.error_msg = "ERROR: file count must be 0 or greater"
      return False

  def stringify_log(self):
    log = '\n'.join(self.log)
    print(log)
    return log

  def check_file_path(self):
    return os.path.isdir(self.file_path)