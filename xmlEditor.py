from __future__ import print_function

import sys
import time
import json
import bs4
from functools import partial
import os
import codecs
import re
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror
basestring = str


__version__ = (0, 2)
debug = False

# default options
opt = {
    'dir': None  # last seen directory
}


class FilePicker(tk.Frame):
    def __init__(self, master, command=None):
        tk.Frame.__init__(self, master)
        self.command = command

        hlm = tk.Frame(self)
        hlm.pack(fill=tk.X, expand=tk.TRUE)
        self.fold = AutoSelectEntry(hlm, command=self.browse)
        self.fold.pack(side=tk.LEFT, fill=tk.X, expand=tk.TRUE)
        btn = ttk.Button(hlm, text="...", width=3, command=self.browse)
        btn.pack(side=tk.LEFT)

        hlm = tk.Frame(self)
        hlm.pack(fill=tk.X, expand=tk.TRUE)
        self.file = tk.StringVar(self)
        self.file.set("Select a File")
        self.files = ttk.OptionMenu(hlm, self.file)
        self.files.pack(side=tk.LEFT, fill=tk.X, expand=True)

        btn = ttk.Button(hlm, text="Save", command=master.save)
        btn.pack(side=tk.LEFT)

    def update_options(self, options):
        self.files['menu'].delete(0, tk.END)
        for option in options:
            self.files['menu'].add_command(
                label=option, command=partial(self.run_command, option))
        self.file.set("Select a File")

    def run_command(self, fn):
        try:
            if self.command:
                self.command(os.path.join(self.fold.get(), fn))
            self.file.set(fn)
        except Exception as e:
            showerror("File Load Error",
                      "%s is not a valid XML file.\n%s" % (fn, e))
            if debug:
                raise

    def browse(self, dir=None):
        if dir is None:
            dir = askdirectory(initialdir=opt.get('dir'))
        if dir:  # check for user cancelled
            result = self.load_dir(dir)
            if hasattr(self.master, 'status'):
                self.master.status.set(result)

    def load_dir(self, dir):
        try:
            fns = os.listdir(dir)
        except Exception as e:
            print("could not load folder:", e)
            return "invalid folder"
        opt['dir'] = dir
        self.fold.set(dir)
        file_types = [".xml"]
        dir = [fn for fn in fns if any(fn.endswith(x) for x in file_types)]
        self.update_options(dir)
        return "{} files found".format(len(dir))

    def load_path(self, path):
        dir, fn = os.path.split(path)
        self.load_dir(dir)
        self.run_command(fn)


class VerticalScrolledFrame:
    """
    A vertically scrolled Frame that can be treated like any other Frame
    ie it needs a master and layout and it can be a master.
    keyword arguments are passed to the underlying Canvas (eg width, height)
    """

    def __init__(self, master, **kwargs):
        self.outer = tk.Frame(master)

        self.vsb = tk.Scrollbar(self.outer, orient=tk.VERTICAL)
        self.vsb.pack(fill=tk.Y, side=tk.RIGHT)
        self.canvas = tk.Canvas(self.outer, highlightthickness=0, **kwargs)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas['yscrollcommand'] = self.vsb.set
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb['command'] = self.canvas.yview

        self.inner = tk.Frame(self.canvas)
        # pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(tk.Widget))
        self.frames = (self.inner, self.outer)

    def __getattr__(self, item):
        """geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
        all other attributes (_w, children, etc) are passed to self.inner"""
        return getattr(self.frames[item in self.outer_attr], item)

    def _on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _bind_mouse(self, event=None):
        """mouse event bind does not work, so this hack allows the use of bind_all
        Linux uses Buttons, Windows/Mac uses MouseWheel"""
        for ev in ("<Button-4>", "<Button-5>", "<MouseWheel>"):
            self.canvas.bind_all(ev, self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        for ev in ("<Button-4>", "<Button-5>", "<MouseWheel>"):
            self.canvas.unbind_all(ev)

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1, "units")


class AutoSelectEntry(ttk.Entry):
    elements = []

    def __init__(self, master, command=None, **kwargs):
        """Entry widget that auto selects when focused
        command is a function to execute on value change"""
        ttk.Entry.__init__(self, master, **kwargs)
        self.command = command
        self.old_value = None
        self.elements.append(self)
        self.dirty = False

        self.bind('<FocusIn>', self.select_all)
        self.bind('<Return>', self.input_change)
        self.bind('<FocusOut>', self.input_change)

    def select_all(self, event=None):
        self.selection_range(0, tk.END)

    def input_change(self, event=None, value=None):
        if value is None:
            value = self.get()
        if self.command is not None:
            if value == self.old_value:
                return  # check for a change; prevent command trigger when just tabbing through
            self.dirty = True
            self.old_value = value
            self.command(value)
        self.select_all()

    def set(self, text=None, run=False):
        if text is None:
            text = ""
        if len(text) > 500:
            text = "<too long to display>"
        self.delete(0, tk.END)
        self.insert(0, text)
        self.old_value = text
        if run:
            self.input_change(text)


class GUI(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.fn = None
        self.bs = None
        master.title("Config File Editor")
        master.geometry("800x600")
        master.protocol('WM_DELETE_WINDOW', self._quit)
        master.bind("<Control - S>", self.save)
        master.bind("<Control - s>", self.save)

        self.top = FilePicker(self, command=self.load_file)
        self.top.pack(fill=tk.X)

        self.top.load_dir(opt.get('dir') or os.getcwd())

        self.data_frame = tk.Frame(self)
        self.display = VerticalScrolledFrame(self.data_frame)
        self.display.pack(fill=tk.BOTH, expand=True)
        self.data_frame.pack(fill=tk.BOTH, expand=True)

        self.status = tk.StringVar(
            self, "Version: "+".".join(map(str, __version__)))
        lbl = ttk.Label(self, textvariable=self.status)
        lbl.pack(fill=tk.X)

    def _quit(self):
        self.master.destroy()

    def load_file(self, fn):
        print('loading', fn)
        self.fn = os.path.normpath(fn)
        AutoSelectEntry.elements = []
        # "rb" mode is python 2 and 3 compatibe; BS handles the unicode conversion.
        with open(fn, 'rb') as f:
            self.bs = bs4.BeautifulSoup(f, 'xml')
        elements, comments = [], []
        for e in self.bs.contents:
            if istag(e):
                elements.append(e)
            elif isinstance(e, basestring):
                comments.append(e)
            else:
                print("WARNING: unidentified elements found:", e)
        if len(elements) > 1:
            print("WARNING: %s root elements found; one expected")
        assert elements, "No XML data found"

        if self.display is not None:
            self.display.destroy()
            del self.display
        start = elements[0]
        self.display = VerticalScrolledFrame(self.data_frame)
        if comments:
            hlm = ttk.LabelFrame(self.display, text="File Comments")
            for comm in comments:
                lbl = tk.Label(hlm, text=comm, anchor='w',
                               wraplength=300, justify=tk.LEFT)
                lbl.pack(fill=tk.X)
            hlm.pack()
        core = self.make_label_frame(self.display, start)
        core.pack()
        self.display.pack(expand=True, fill=tk.BOTH)
        self.status.set("Loaded {} elements".format(
            len(AutoSelectEntry.elements)))

    def save(self, event=None):
        print("Saving data")

        # trigger current variable if needed
        current = self.focus_get()
        if hasattr(current, 'input_change'):
            current.input_change()

        try:
            self.save_core()
        except Exception as e:
            showerror("Save Error", "Could not save file.\n"+str(e))
            if debug:
                raise

    def save_core(self):
        if self.fn is None:
            print("cannot save - no file loaded")
            self.status.set("cannot save - no file loaded")
            return

        encoding = self.bs.original_encoding

        data = self.bs.prettify()
        data = MSiffy(data)
        data = data.replace('\n', '\r\n')  # Windows ... (sigh)
        # BS insists on utf8 output from prettify
        data = data.replace('utf-8', encoding, 1)

        with codecs.open(self.fn, 'w', encoding) as f:
            f.write(data)

        for element in AutoSelectEntry.elements:
            element.dirty = False

        self.status.set("File saved.")

    def make(self, frame, bs):
        children = list(filter(istag, bs.children))
        idx = 0
        num_attributes = len(bs.attrs)
        num_text = 0 if bs.string is None else 1
        if debug:
            print("{}: {} attributes; {} text; {} grandchildren".format(
                bs.name, num_attributes, num_text, len(children)))

        # list out the attributes, then text, then grandchildren.
        for attr, value in bs.attrs.items():
            # attribute entry
            idx = self.make_entry(
                frame, idx, attr, value.strip(), partial(self.change_attr, bs, attr))
        if bs.string is not None:
            # text entry
            idx = self.make_entry(
                frame, idx, "", bs.text.strip(), partial(self.change_attr, bs, None))
        for child in children:
            num_children = len(child.findChildren()) + len(child.attrs)
            if num_children == 0 and child.string is not None:
                # special case of only 1 text - making entry
                idx = self.make_entry(frame, idx, child.name, child.string.strip(), partial(
                    self.change_attr, child, None))
            elif num_children > 0:
                # child has one attribute or one grandchild; make new frame
                h = self.make_label_frame(frame, child)
                h.grid(row=idx, column=0, columnspan=2,
                       sticky='ew', padx=10, pady=10)
                idx += 1
            # else: tag has no children and no text; ignore

    @staticmethod
    def make_entry(master, row, name, value, command):
        lbl = tk.Label(master, text=name, anchor='e')
        lbl.grid(row=row, column=0, sticky='ew')
        ent = AutoSelectEntry(
            master, width=400, command=command)
        ent.set(value)
        ent.grid(row=row, column=1, sticky='e')
        return row + 1

    def make_label_frame(self, master, bs):
        frame = ttk.LabelFrame(master, text=bs.name)
        hlm = tk.Frame(frame)
        hlm.columnconfigure(0, weight=1)
        self.make(hlm, bs)
        hlm.pack(side=tk.RIGHT)
        return frame

    def dirty_status(self):
        changes = "{} unsaved changes".format(
            sum(x.dirty for x in AutoSelectEntry.elements))
        print(changes)
        self.status.set(changes)

    def change_attr(self, bs, attr, new_text):
        if attr is None:
            bs.string = new_text
        else:
            bs[attr] = new_text
        self.dirty_status()


def istag(test):
    return isinstance(test, bs4.Tag)


def MSiffy(data):
    """convert the beautifulsoup prettify output to a microsoft .NET style
    Basically this means moving the contents of tags into the same line as the tag"""
    hlm = []
    state = False
    leading_spaces = re.compile(r"^\s*")
    for line in data.splitlines():
        if "<" in line:
            if state:
                line = line.strip()
            else:
                spaces = leading_spaces.search(line).group(0)
                line = spaces + line
            hlm.append(line)
            state = False
        else:
            hlm.append("\n" + line.strip() + "\n")
            state = True
    nd = "\n".join(hlm)
    return nd.replace("\n\n", "")


def start_xml_editor():
    root = tk.Tk()
    window = GUI(root)
    window.pack(fill=tk.BOTH, expand=True)
    if len(sys.argv) > 1:
        window.top.load_path(" ".join(sys.argv[1:]))
    root.mainloop()

if __name__ == "__main__":
    try:
        start_xml_editor()
    except Exception as e:
        showerror("Fatal error!", "Config Editor crashed.\n\n"+str(e))
