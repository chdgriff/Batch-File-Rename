from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import askyesno
from batch_find_replace import BatchFindReplace
from batch_prepend_append import BatchPrependAppend
from remove_tokens import BatchRemoveTokens

class BatchFileRename(Tk):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.dir_path = StringVar(self)

    container = Frame(self)
    container.pack(fill=BOTH, expand=True)
    
    # Adds header frames
    row_idx = 0
    for F in (ModeButtonsFrame, FilePathFrame):
      F(parent = container, controller = self).grid(row=row_idx, column=0, sticky="W")
      row_idx += 1

    # Main function frames
    self.modes = {}
    for F in (FindandReplaceFrame, RemoveTokenFrame, PrependAppendFrame):
      frame = F(parent = container, controller = self)
      self.modes[F.__name__] = frame
      frame.grid(row=row_idx, column=0, sticky="nsew")

    # Default Frame
    self.show_frame("FindandReplaceFrame")

  def show_frame(self, page_name):
    self.modes[page_name].tkraise()
    
class ModeButtonsFrame(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)

    # Buttons for all the modes
    find_replace_btn = Button(self, text = "Find and Replace", command = lambda: controller.show_frame("FindandReplaceFrame"))
    remove_token_btn = Button(self, text = "Remove Token", command = lambda: controller.show_frame("RemoveTokenFrame"))
    prepend_append_btn = Button(self, text = "Prepend or Append", command = lambda: controller.show_frame("PrependAppendFrame"))    
    
    # Packs the buttons on the frame
    find_replace_btn.pack(side=LEFT)
    remove_token_btn.pack(side=LEFT)
    prepend_append_btn.pack(side=LEFT)

class FilePathFrame(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.controller = controller

    # Entries for browse directory field
    label      = Label(self, text="Directory:")
    self.field = Entry(self, bd = 5, textvariable=controller.dir_path, width=100)
    browse_btn = Button(self, text="...", command=self.browse_directories)

    # Packs the entries on the frame
    label.pack(side=LEFT)
    self.field.pack(side=LEFT)
    browse_btn.pack(side=LEFT)

  def browse_directories(self):
    input_dir_path = filedialog.askdirectory()
    if input_dir_path:
      self.controller.dir_path.set(input_dir_path)
      
class FindandReplaceFrame(Frame):
  def __init__(self, parent, controller):
    self.controller = controller
    super().__init__(parent)

    # All the input field variables
    self.find_text = StringVar(self, "")
    self.offset = StringVar(self, '0')
    self.replace_text = StringVar(self, "")
    self.file_count = StringVar(self, 0)
    self.ignore_case = BooleanVar(self, False)
    self.overwrite_file_ext = BooleanVar(self, False)
    self.log = StringVar(self)

    # Container setup
    container = Frame(self)
    container.pack(expand=True, fill=BOTH)
    container.columnconfigure(0, weight=1)
    container.rowconfigure(1, weight=1)

    # Child frames
    _FindandReplaceFields(parent=container, controller=self).grid(row=0, column=0, sticky="W")
    Log(parent=container, controller=self).grid(row=1, column=0)
    RunButtons(parent=container, controller=self, function=self.call_find_replace).grid(row=2, column=0)

  def call_find_replace(self, debug=True):
    self.log.set(BatchFindReplace(self.controller.dir_path.get(), self.find_text.get(), int(self.offset.get()), self.replace_text.get(), bool(self.ignore_case.get()), bool(self.overwrite_file_ext.get()), self.file_count.get(), debug).run())

class _FindandReplaceFields(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)

    # All the entries
    find_field = Entry(self, bd=2, textvariable=controller.find_text, width=50)
    overwrite_file_ext_field = Checkbutton(self, offvalue=False, onvalue=True, variable=controller.overwrite_file_ext)
    offset_field = Entry(self, bd=2, width=3, textvariable=controller.offset)
    ignore_case_field = Checkbutton(self, offvalue=False, onvalue=True, variable=controller.ignore_case)
    replace_field = Entry(self, bd=2, textvariable=controller.replace_text, width=50)
    file_count_field = Entry(self, bd=2, width=3, textvariable=controller.file_count)

    # Adds the entries and labels to the grid 
    Label(self, text="Find: ").grid(row=0, column=0, sticky="W")
    find_field.grid(row=0, column=1)
    Label(self, text="Overwrite File Extension: ").grid(row=0, column=2, sticky="W")
    overwrite_file_ext_field.grid(row=0, column=3, sticky="W")
    Label(self, text="Offset:").grid(row=1, column=0, sticky="W")
    offset_field.grid(row=1, column=1, sticky="W")
    Label(self, text="Ignore Case: ").grid(row=1, column=2, sticky="W")
    ignore_case_field.grid(row=1, column=3, sticky="W")
    Label(self, text="Replace: ").grid(row=2, column=0, sticky="W")
    replace_field.grid(row=2, column=1)
    Label(self, text="File Count: ").grid(row=3, column= 0, sticky="W")
    file_count_field.grid(row=3, column=1, sticky="W")

class PrependAppendFrame(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.controller = controller

    self.text = StringVar(self, "")
    self.prepend_append = StringVar(self, "Prepend")
    self.file_count = StringVar(self, 0)
    self.log = StringVar(self)

    # Container setup
    container = Frame(self)
    container.pack(expand=True, fill=BOTH)
    container.columnconfigure(0, weight=1)
    container.rowconfigure(1, weight=1)

    _PrependAppendFields(parent=container, controller=self).grid(row=0, column=0, sticky="W")
    Log(parent=container, controller=self).grid(row=1, column=0)
    RunButtons(parent=container, controller=self, function=self.call_prepend_append).grid(row=2, column=0)

  def call_prepend_append(self, debug=True):
    prepend_append = 'A' if self.prepend_append.get() == "Append" else 'P'

    self.log.set(BatchPrependAppend(self.controller.dir_path.get(), self.text.get(), prepend_append, self.file_count.get(), debug).run())

class _PrependAppendFields(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)

    text_field = Entry(self, bd=2, textvariable=controller.text, width=50)
    prepend_append_dropdown = OptionMenu(self, controller.prepend_append, "Prepend", "Append")
    file_count_field = Entry(self, bd=2, width=3, textvariable=controller.file_count)
    
    Label(self, text="Text: ").grid(row=0, column=0, sticky="W")
    text_field.grid(row=0, column=1)
    prepend_append_dropdown.grid(row=0, column=2)
    Label(self, text="File Count: ").grid(row=1, column= 0, sticky="W")
    file_count_field.grid(row=1, column=1, sticky="W")

class RemoveTokenFrame(Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.controller = controller

    # Input field variables
    self.token = StringVar(self, '.')
    self.file_count = StringVar(self, 0)
    self.log = StringVar(self)

    # Container setup
    container = Frame(self)
    container.pack(expand=True, fill=BOTH)
    container.columnconfigure(0, weight=1)
    container.rowconfigure(1, weight=1)

    # All the child frames
    _RemoveTokenFields(container, self,).grid(row=0, column=0, sticky="W")
    Log(parent=container, controller=self).grid(row=1, column=0)
    RunButtons(parent=container, controller=self, function=self.call_remove_token).grid(row=2, column=0)
  
  def call_remove_token(self, debug=True):
    self.log.set(BatchRemoveTokens(self.controller.dir_path.get(), int(self.file_count.get()), self.token.get(), debug).run())

class _RemoveTokenFields(Frame):
  def __init__(self, parent, controller) -> None:
    super().__init__(parent)
    
    # Input fields
    token_field = Entry(self, bd=2, width=3, textvariable=controller.token)
    file_count_field = Entry(self, bd=2, width=3, textvariable=controller.file_count)
    
    # Adds labels and input fields to grid
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
    Button(self, text="Save Adjustments", command=lambda: self.confirm_save(function)).pack(side=LEFT)

  def confirm_save(self, function):
    """
    Pops confirmation dialog. On yes runs passed function otherwise does nothing.

    :param function: This is called on confirmation as function(debug=False)
    """
    if askyesno(title="Confirmation", message= "Are you sure you want to rename the files?"):
      function(debug=False)

def main():
  app = BatchFileRename()
  app.title("Batch String Formatting")
  app.mainloop()

if __name__ == '__main__':
  main()