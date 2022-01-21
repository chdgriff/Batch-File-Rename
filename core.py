class BatchFileOperations():
  def __init__(self, file_path, file_count, debug=True) -> None:
      self.file_path = file_path
      self.file_count = file_count
      self.debug = debug
      self.log = []
      self.error_msg = ""