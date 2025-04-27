import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import tkinter.simpledialog as sd

app_name = "C.I.R.Q.C.S."  # Code In Repository Quality Checking Service


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
        self.status.configure(text=status)
        self.update()


class Application:
    def __init__(self, remarks, base_path):
        self.remark_info = remarks
        self.all_type_text = " [ All ]"
        self.sel_evaluator = None
        self.sel_file = None
        self.sel_type = None

        self.root = tk.Tk()
        self.root.title(f"{app_name} - {base_path}")

        self.upper_menu = tk.LabelFrame(self.root, padx=2, pady=5)
        self.button_clipboard = ttk.Button(self.upper_menu, text="Copy remarks to clipboard")
        self.button_exit = ttk.Button(self.upper_menu, text="Exit", command=quit)

        self.surface = ttk.Frame(padding=5)
        self.sub_surface = ttk.Frame(self.surface)
        self.sub_frame = tk.LabelFrame(self.sub_surface, padx=2, pady=2)
        self.general_comment = tk.Label(self.sub_frame, text="")
        self.evaluators = tk.Listbox(self.surface, exportselection=0, width=20)
        self.file_paths = tk.Listbox(self.sub_surface, exportselection=0, width=40)
        self.remark_types = tk.Listbox(self.sub_surface, exportselection=0, width=40)
        self.remarks = tk.Listbox(self.sub_surface, exportselection=0, selectmode="extended", width=120)
        self.remark_scrollbar = ttk.Scrollbar(self.sub_surface)

        self.upper_menu.pack(side="top", fill="x")
        self.button_clipboard.pack(side="left")
        self.button_exit.pack(side="right")

        self.surface.pack(fill="both", expand=True)
        self.evaluators.pack(side="left", fill="y")
        self.sub_surface.pack(fill="both", expand=True)
        self.sub_frame.pack(side="top", fill="x", padx=1, pady=1)
        self.general_comment.grid(row=0, column=0)
        self.file_paths.pack(side="left", fill="y")
        self.remark_types.pack(side="left", fill="y")
        self.remarks.pack(side="left", fill="both", expand=True)
        self.remark_scrollbar.pack(side="right", fill="y")

        self.remarks.configure(yscrollcommand=self.remark_scrollbar.set)
        self.remark_scrollbar.configure(command=self.remarks.yview)
        self.button_clipboard.config(command=self.copy_to_clipboard)
        self.evaluators.bind("<<ListboxSelect>>", lambda _: self.click_evaluators())
        self.file_paths.bind("<<ListboxSelect>>", lambda _: self.click_files())
        self.remark_types.bind("<<ListboxSelect>>", lambda _: self.click_types())

        self.evaluators.insert(0, *self.remark_info.keys())
        if self.evaluators.size() > 0:
            self.evaluators.select_set(0)
            self.click_evaluators()

    def update_selection(self):
        idx_evaluator = self.evaluators.curselection()
        idx_file = self.file_paths.curselection()
        idx_type = self.remark_types.curselection()

        self.sel_evaluator = self.evaluators.get(idx_evaluator[0]) if idx_evaluator else None
        self.sel_file = self.file_paths.get(idx_file[0]) if idx_file else None
        self.sel_type = self.remark_types.get(idx_type[0]) if idx_type else None

    def clean(self, files=False, types=False, remarks=False):
        if files:
            self.file_paths.delete(0, tk.END)
        if types:
            self.remark_types.delete(0, tk.END)
        if remarks:
            self.remarks.delete(0, tk.END)

    def click_evaluators(self):
        self.update_selection()
        self.fill_files()

        if self.file_paths.size() > 0:
            self.file_paths.select_set(0)
            self.click_files()

    def fill_files(self):
        gen_remark = self.remark_info[self.sel_evaluator]
        self.general_comment.configure(text=gen_remark.general_rem)

        files = list(gen_remark.files.keys())
        if len(files) > 1:
            files = [self.all_type_text] + files

        self.clean(True, True, True)
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
        r_types = evaluator.get_all_r_types(file_name)
        if len(r_types) > 1:
            r_types = [self.all_type_text] + r_types

        self.clean(False, True, True)
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

        self.clean(False, False, True)
        self.remarks.insert(0, *rem_text)

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
