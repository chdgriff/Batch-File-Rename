from tkinter import *
from tkinter import filedialog

class BatchFileRename(Tk):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.file_path = StringVar()
    
    container = Frame(self)
    container.pack(fill=BOTH, expand=True)
    
    row_idx = 0
    for F in (ModeButtons, FilePath):
      F(parent = container, controller = self).grid(row=row_idx, column=0, sticky="W")
      row_idx += 1

    self.modes = {}
    for F in (FindandReplace, PrependAppend):
      frame = F(parent = container, controller = self)
      self.modes[F.__name__] = frame
      frame.grid(row=row_idx, column=0, sticky="nsew")

    self.show_frame("FindandReplace")

  def show_frame(self, page_name):
    self.modes[page_name].tkraise()
    

class ModeButtons(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)

    find_replace_btn = Button(self, text = "Find and Replace", command = lambda: controller.show_frame("FindandReplace"))
    prepend_append_btn = Button(self, text = "Prepend or Append", command = lambda: controller.show_frame("PrependAppend"))

    find_replace_btn.pack(side=LEFT)
    prepend_append_btn.pack(side=LEFT)


class FilePath(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.file_path = StringVar()

    label      = Label(self, text="Directory:")
    self.field = Entry(self, bd = 5, textvariable=controller.file_path, width=100)
    browse_btn = Button(self, text="...", command=self.browse_directories)

    label.pack(side=LEFT)
    self.field.pack(side=LEFT)
    browse_btn.pack(side=LEFT)

  def browse_directories(self):
    self.field.delete(0)
    self.field.insert(0, filedialog.askdirectory())
      
class FindandReplace(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)

    self.find_text = StringVar(self)
    self.offset = StringVar(self, '0')
    self.replace_text = StringVar(self)
    self.file_count = StringVar(self, '0')

    container = Frame(self)
    container.pack(expand=True, fill=BOTH)
    container.columnconfigure(0, weight=1)
    container.rowconfigure(1, weight=1)
    _FindandReplaceFields(parent=container, controller=self).grid(row=0, column=0, sticky="W")
    Log(parent=container, controller=self, message="").grid(row=1, column=0, sticky="NSEW")
    _FindandReplaceButtons(parent=container, controller=self).grid(row=2, column=0)

  def call_find_replace(self, debug=True):
    pass

class _FindandReplaceFields(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)

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

class _FindandReplaceButtons(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    Button(self, text="Test Adjustments").pack(side=LEFT)
    Button(self, text="Save Adjustments").pack(side=LEFT)

class PrependAppend(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)

    Label(self, text="Prepend or Append").pack()

class Log(Frame):
  def __init__(self, parent, controller, message=""):
    super().__init__(parent, width=100, height=100, bg="white")

    Message(self, bg="white", justify=LEFT, text=message).pack(expand=True)

def main():
  app = BatchFileRename()
  app.title("Batch String Formatting")
  app.mainloop()

if __name__ == '__main__':
  main()