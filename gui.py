from cgitb import text
from tkinter import *
from tkinter import filedialog

class BatchFileRename(Tk):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    container = Frame(self)
    container.pack(fill=BOTH, expand=True)
    
    row_idx = 0
    for F in (ModeButtons, FilePath):
      F(parent = container, controller = self).grid(row=row_idx, column=0)
      row_idx += 1

    self.modes = {}
    for F in (FindandReplace, PrependAppend):
      frame = F(parent = container, controller = self)
      self.modes[F.__name__] = frame
      frame.grid(row=row_idx, column=0, sticky="nsew")

    self.showFrame("FindandReplace")

  def showFrame(self, page_name):
    self.modes[page_name].tkraise()
    

class ModeButtons(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)

    find_replace_btn = Button(self, text = "Find and Replace", command = lambda: controller.showFrame("FindandReplace"))
    prepend_append_btn = Button(self, text = "Prepend or Append", command = lambda: controller.showFrame("PrependAppend"))

    find_replace_btn.pack(side=LEFT)
    prepend_append_btn.pack(side=LEFT)


class FilePath(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.file_path = ""

    label      = Label(self, text="Directory:")
    self.field = Entry(self, bd = 5, textvariable=self.file_path, width=100)
    browse_btn = Button(self, text="...", command=self.browseDirectories)

    label.pack(side=LEFT)
    self.field.pack(side=LEFT)
    browse_btn.pack(side=LEFT)

  def browseDirectories(self):
    self.field.delete(0)
    self.field.insert(0, filedialog.askdirectory())
      
class FindandReplace(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)

    self.find_text = ""
    self.offset = '0'
    self.replace_text = ""

    find_field = Entry(self, bd=5, textvariable=self.find_text, width=50)
    offset_field = Entry(self, bd=5, width=3, textvariable=self.offset)
    offset_field.insert(0, self.offset)
    replace_field = Entry(self, bd=5, textvariable=self.replace_text, width=50)


    Label(self, text="Find:").grid(row=0, column=0)
    find_field.grid(row=0, column=1)
    Label(self, text="Offset:").grid(row=1, column=0)
    offset_field.grid(row=1, column=1, sticky="W")
    Label(self, text="Replace:").grid(row=2, column=0)
    replace_field.grid(row=2, column=1)

class PrependAppend(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)

    Label(self, text="Prepend or Append").pack()

def main():
  app = BatchFileRename()
  app.mainloop()

if __name__ == '__main__':
  main()