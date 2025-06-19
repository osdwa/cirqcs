import tkinter as tk
import tkinter.ttk as ttk
from gui_elements import *
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import tkinter.simpledialog as sd

from xml_report import report_to_xml, xml_to_report

app_name = "C.I.R.Q.C.S."  # Code In Repository Quality Checking Service

types_xml = [
    ("XML file", "*.xml"),
    ("All files", "*.*")
]


class PathChooser(sd.Dialog):
    def body(self, master):
        self.result = None

        general_label = tk.Label(master, text="Enter your GitHub/GitLab repository URL or local repository path.")
        input_field = tk.Frame(master)
        self.input_url = ttk.Entry(input_field)
        input_browse = ttk.Button(input_field, text="Browse (local)", command=self.browse)

        general_label.pack(fill="x", expand=True)
        input_field.pack(fill="x", expand=True)
        self.input_url.pack(side="left", fill="x", expand=True)
        input_browse.pack(side="right")

    def browse(self):
        if path := fd.askdirectory():
            self.input_url.delete(0, tk.END)
            self.input_url.insert(0, str(path))

    def apply(self):
        self.result = self.input_url.get()


class SplashScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(app_name)
        self.geometry("300x200")
        self.resizable(False, False)

        self.surface = tk.Frame(self)
        self.please_wait = tk.Label(self.surface, text="Please wait...")
        self.status = tk.Label(self.surface, text="---")

        self.surface.place(relx=0.5, rely=0.5, anchor="center")
        self.please_wait.pack()
        self.status.pack()

    def set_status(self, status):
        print("Splash:", status)
        self.status.configure(text=status)
        self.update()


class Application:
    def __init__(self):
        self.remark_label = ""
        self.remark_info = {}
        self.all_type_text = " [ All ]"
        self.sel_evaluator = None
        self.sel_file = None
        self.sel_type = None

        self.root = tk.Tk()
        self.root.title(app_name)

        self.upper_menu = tk.Frame(self.root, bg="#2e2e2e", padx=2, pady=5)
        self.button_export = Button(self.upper_menu, text="Export as XML", width=15)
        self.button_import = Button(self.upper_menu, text="Import XML", width=15)
        self.button_clipboard = Button(self.upper_menu, text="Copy remarks to clipboard")
        self.button_exit = Button(self.upper_menu, text="Exit", width=10, command=quit)

        self.surface = tk.Frame(self.root, bg="#2e2e2e", padx=5, pady=5)
        self.sub_surface = tk.Frame(self.surface, bg="#2e2e2e")
        self.sub_frame1 = tk.Frame(self.sub_surface, bg="#444", padx=1, pady=1)
        self.sub_frame2 = tk.Frame(self.sub_frame1, bg="#2e2e2e", padx=2, pady=2)
        self.general_comment = tk.Label(self.sub_frame2, font="Arial 12 bold", fg="white", bg="#2e2e2e", text="")
        self.evaluators = Listbox(self.surface, font="Arial 12 bold", exportselection=0, width=10)
        self.file_paths = Listbox(self.sub_surface, exportselection=0, width=30)
        self.remark_types = Listbox(self.sub_surface, exportselection=0, width=25)
        self.remarks = Listbox(self.sub_surface, fg="#FF3030", sfg="#FFA0A0", font="{Courier New} 11 bold",
                               exportselection=0, selectmode="extended")
        self.remark_scrollbar = ttk.Scrollbar(self.sub_surface)

        self.upper_menu.pack(side="top", fill="x")
        self.button_export.pack(side="left", padx=1)
        self.button_import.pack(side="left", padx=1)
        self.button_clipboard.pack(side="left", padx=1)
        self.button_exit.pack(side="right", padx=1)

        self.surface.pack(fill="both", expand=True)
        self.evaluators.pack(side="left", fill="y")
        self.sub_surface.pack(fill="both", expand=True)
        self.sub_frame1.pack(side="top", fill="x", padx=1)
        self.sub_frame2.pack(fill="both", expand=True)
        self.general_comment.grid(row=0, column=0)
        self.file_paths.pack(side="left", fill="y", padx=1)
        self.remark_types.pack(side="left", fill="y")
        self.remarks.pack(side="left", fill="both", expand=True)
        self.remark_scrollbar.pack(side="right", fill="y")

        self.remarks.configure(yscrollcommand=self.remark_scrollbar.set)
        self.remark_scrollbar.configure(command=self.remarks.yview)
        self.button_export.config(command=self.save_to_xml)
        self.button_import.config(command=self.read_from_xml)
        self.button_clipboard.config(command=self.copy_to_clipboard)
        self.evaluators.bind("<<ListboxSelect>>", lambda _: self.click_evaluators())
        self.file_paths.bind("<<ListboxSelect>>", lambda _: self.click_files())
        self.remark_types.bind("<<ListboxSelect>>", lambda _: self.click_types())
        self.remarks.bind("<Return>", lambda _: self.click_remarks())
        self.remarks.bind("<Double-Button-1>", lambda _: self.click_remarks())

    def update_content(self, remarks, base_path):
        self.root.title(f"{app_name} - {base_path}")
        self.remark_label = str(base_path)
        self.remark_info = remarks

        self.fill_evaluators()

    def update_selection(self):
        idx_evaluator = self.evaluators.curselection()
        idx_file = self.file_paths.curselection()
        idx_type = self.remark_types.curselection()

        self.sel_evaluator = self.evaluators.get(idx_evaluator[0]) if idx_evaluator else None
        self.sel_file = self.file_paths.get(idx_file[0]) if idx_file else None
        self.sel_type = self.remark_types.get(idx_type[0]) if idx_type else None

    def clean(self, evaluators, files, types, remarks):
        if evaluators:
            self.evaluators.delete(0, tk.END)
        if files:
            self.file_paths.delete(0, tk.END)
        if types:
            self.remark_types.delete(0, tk.END)
        if remarks:
            self.remarks.delete(0, tk.END)

    def fill_evaluators(self):
        self.clean(True, True, True, True)

        self.evaluators.insert(0, *self.remark_info.keys())
        if self.evaluators.size() > 0:
            self.evaluators.select_set(0)
            self.click_evaluators()

    def click_evaluators(self):
        self.update_selection()
        self.fill_files()

        if self.file_paths.size() > 0:
            self.file_paths.select_set(0)
            self.click_files()

    def fill_files(self):
        if self.sel_evaluator is None:
            return

        gen_remark = self.remark_info[self.sel_evaluator]
        self.general_comment.configure(text=gen_remark.general_rem)

        files = sorted(gen_remark.files)
        if len(files) > 1:
            files = [self.all_type_text] + files

        self.clean(False, True, True, True)
        self.file_paths.insert(0, *files)

    def click_files(self):
        self.update_selection()
        self.fill_types()

        if self.remark_types.size() > 0:
            self.remark_types.select_set(0)
            self.click_types()

    def fill_types(self):
        if self.sel_evaluator is None or self.sel_file is None:
            return

        evaluator = self.remark_info[self.sel_evaluator]
        file_name = self.sel_file if self.sel_file != self.all_type_text else None
        r_types = evaluator.get_all_r_long_types(file_name)
        if len(r_types) > 1:
            r_types = [self.all_type_text] + r_types

        self.clean(False, False, True, True)
        self.remark_types.insert(0, *r_types)

    def click_types(self):
        self.update_selection()
        self.fill_remarks()

    def fill_remarks(self):
        if self.sel_evaluator is None or self.sel_file is None or self.sel_type is None:
            return

        all_files = (self.sel_file == self.all_type_text)
        all_types = (self.sel_type == self.all_type_text)

        sel_file = None if all_files else self.sel_file
        sel_type = None if all_types else self.sel_type

        remarks = self.remark_info[self.sel_evaluator].filtered(sel_file, sel_type)
        rem_text = []
        for remark in remarks:
            lines = remark.get_as_text(all_files, all_types)
            rem_text.extend(lines.split("\n"))

        self.clean(False, False, False, True)
        self.remarks.insert(0, *rem_text)

    def click_remarks(self):
        select = self.remarks.curselection()

        if len(select) == 1:
            sel_text = self.remarks.get(select[0])
            mb.showinfo(app_name, sel_text)

    def save_to_xml(self):
        path = fd.asksaveasfilename(defaultextension="xml", filetypes=types_xml)
        if not path:
            return

        report_to_xml(path, self.remark_label, self.remark_info)

    def read_from_xml(self):
        path = fd.askopenfilename(defaultextension="xml", filetypes=types_xml)
        if not path:
            return

        label, rem_info = xml_to_report(path)
        self.update_content(rem_info, label)

    def copy_to_clipboard(self):
        if self.sel_evaluator is None or self.sel_file is None or self.sel_type is None:
            pass

        select = self.remarks.curselection()
        if not select:
            select = range(self.remarks.size())

        content = "\n".join(self.remarks.get(selected) for selected in select)
        self.root.clipboard_clear()
        self.root.clipboard_append(content)

    def mainloop(self):
        self.root.mainloop()
