import os

class BatchFileOperations():
  def __init__(self, file_path, file_count, debug=True) -> None:
      self.file_path = file_path
      self.file_count = file_count
      self.debug = debug
      self.log = []
      self.error_msg = ""
  
  def stringify_log(self):
    return '\n'.join(self.log)
    
  def check_file_path(self):
    return os.path.isdir(self.file_path)