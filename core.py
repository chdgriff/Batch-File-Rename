import os

class BatchFileNameOperations():
  """
  Contains core functions and variables.


  -----------
  Attributes:
  -----------
  dir_path : str
    The path to files.
  file_count : int
    The number of files to run the operations on.
  debug : bool
    Whether to just print the log or write out file name operations (default True).
  
  --------
  Methods:
  --------
  check_core_vars() --> bool
    Runs error checking on the core variables.
  stringify_log() --> str
  """
  def __init__(self, dir_path, file_count, debug=True) -> None:
    self.dir_path = dir_path
    self.file_count = file_count
    self.debug = debug
    self.log = []
    self.error_msg = ""
  
  def check_core_vars(self) -> bool:
    """Runs error checking on the core variables."""
    if not self._check_dir_path():
      self.error_msg = "ERROR: \""+self.dir_path+"\" cannot be found"
      return False
    if self.file_count < 0:
      self.error_msg = "ERROR: file count must be 0 or greater"
      return False
    return True

  def stringify_log(self) -> str:
    """Converts log from list to string"""
    log = '\n'.join(self.log)
    print(log)
    return log

  def _check_dir_path(self) -> bool:
    """Checks if directory exists"""
    return os.path.isdir(self.dir_path)