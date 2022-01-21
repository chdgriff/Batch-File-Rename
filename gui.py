from tkinter import *
from tkinter import filedialog
from batch_find_replace import BatchFindReplace
from remove_tokens import BatchRemoveTokens

class BatchFileRename(Tk):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.file_path = StringVar(self, "D:/Downloads/Euphoria")
    
    container = Frame(self)
    container.pack(fill=BOTH, expand=True)
    
    row_idx = 0
    for F in (ModeButtonsFrame, FilePathFrame):
      F(parent = container, controller = self).grid(row=row_idx, column=0, sticky="W")
      row_idx += 1

    self.modes = {}
    for F in (FindandReplaceFrame, RemoveTokenFrame, PrependAppendFrame):
      frame = F(parent = container, controller = self)
      self.modes[F.__name__] = frame
      frame.grid(row=row_idx, column=0, sticky="nsew")

    self.show_frame("FindandReplaceFrame")

  def show_frame(self, page_name):
    self.modes[page_name].tkraise()
    
class ModeButtonsFrame(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)

    find_replace_btn = Button(self, text = "Find and Replace", command = lambda: controller.show_frame("FindandReplaceFrame"))
    remove_token_btn = Button(self, text = "Remove Token", command = lambda: controller.show_frame("RemoveTokenFrame"))
    prepend_append_btn = Button(self, text = "Prepend or Append", command = lambda: controller.show_frame("PrependAppendFrame"))    

    find_replace_btn.pack(side=LEFT)
    remove_token_btn.pack(side=LEFT)
    prepend_append_btn.pack(side=LEFT)

class FilePathFrame(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)

    label      = Label(self, text="Directory:")
    self.field = Entry(self, bd = 5, textvariable=controller.file_path, width=100)
    browse_btn = Button(self, text="...", command=self.browse_directories)

    label.pack(side=LEFT)
    self.field.pack(side=LEFT)
    browse_btn.pack(side=LEFT)

  def browse_directories(self):
    self.field.delete(0)
    self.field.insert(0, filedialog.askdirectory())
      
class FindandReplaceFrame(Frame):
  def __init__(self, parent, controller):
    self.controller = controller
    super().__init__(parent)

    self.find_text = StringVar(self, "euphoria.us.s02e01.1080p.web.h264-cakes")
    self.offset = StringVar(self, '0')
    self.replace_text = StringVar(self, "Euphoria")
    self.file_count = StringVar(self, '0')
    self.log = StringVar(self)

    container = Frame(self)
    container.pack(expand=True, fill=BOTH)
    container.columnconfigure(0, weight=1)
    container.rowconfigure(1, weight=1)

    _FindandReplaceFields(parent=container, controller=self).grid(row=0, column=0, sticky="W")
    Log(parent=container, controller=self).grid(row=1, column=0)
    RunButtons(parent=container, controller=self, function=self.call_find_replace).grid(row=2, column=0)

  def call_find_replace(self, debug=True):
    self.log.set(BatchFindReplace(self.controller.file_path.get(), self.find_text.get(), int(self.offset.get()), self.replace_text.get(), int(self.file_count.get()), debug).run())

class _FindandReplaceFields(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    # self.controller = controller

    find_field = Entry(self, bd=2, textvariable=controller.find_text, width=50)
    offset_field = Entry(self, bd=2, width=3, textvariable=controller.offset)
    replace_field = Entry(self, bd=2, textvariable=controller.replace_text, width=50)
    file_count_field = Entry(self, bd=2, width=3, textvariable=controller.file_count)

    Label(self, text="Find:").grid(row=0, column=0, sticky="W")
    find_field.grid(row=0, column=1)
    Label(self, text="Offset:").grid(row=1, column=0, sticky="W")
    offset_field.grid(row=1, column=1, sticky="W")
    Label(self, text="Replace:").grid(row=2, column=0, sticky="W")
    replace_field.grid(row=2, column=1)
    Label(self, text="File Count:").grid(row=3, column= 0, sticky="W")
    file_count_field.grid(row=3, column=1, sticky="W")

class PrependAppendFrame(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)

    Label(self, text="Prepend or Append").pack()

class RemoveTokenFrame(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.controller = controller

    self.token = StringVar(self, '.')
    self.file_count = StringVar(self, '0')
    self.log = StringVar(self)

    container = Frame(self)
    container.pack(expand=True, fill=BOTH)
    container.columnconfigure(0, weight=1)
    container.rowconfigure(1, weight=1)

    _RemoveTokenFields(container, self,).grid(row=0, column=0, sticky="W")
    Log(parent=container, controller=self).grid(row=1, column=0)
    RunButtons(parent=container, controller=self, function=self.call_remove_token).grid(row=2, column=0)
  
  def call_remove_token(self, debug=True):
    self.log.set(BatchRemoveTokens(self.controller.file_path.get(), int(self.file_count.get()), self.token.get(), debug))

class _RemoveTokenFields(Frame):
  def __init__(self, parent, controller) -> None:
    super().__init__(parent)
    
    token_field = Entry(self, bd=2, width=3, textvariable=controller.token)
    file_count_field = Entry(self, bd=2, width=3, textvariable=controller.file_count)
    
    Label(self, text="Token:").grid(row=0, column=0, sticky="W")
    token_field.grid(row=0, column=1, sticky="W")
    Label(self, text="File Count:").grid(row=1, column= 0, sticky="W")
    file_count_field.grid(row=1, column=1, sticky="W")

# class PrependAppend(Frame):
#   def __init__(self, parent, controller):
#     super().__init__(parent)

#     Label(self, text="Prepend or Append").pack()

class Log(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent, bg="white")

    Message(self, bg="white", justify=LEFT, aspect=500, textvariable=controller.log).pack()

class RunButtons(Frame):
  def __init__(self, parent, controller, function):
    super().__init__(parent)
    Button(self, text="Test Adjustments", command=lambda: function()).pack(side=LEFT)
    Button(self, text="Save Adjustments", command=lambda: function(debug=False)).pack(side=LEFT)

def main():
  app = BatchFileRename()
  app.title("Batch String Formatting")
  app.mainloop()

if __name__ == '__main__':
  main()