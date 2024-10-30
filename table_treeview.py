import tkinter as tk
from tkinter import ttk
import pandas as pd
import styles

class EditableTreeviewGadget(tk.Frame):
    def __init__(self, parent, max_width=400, min_height=300,
                dataframe: pd.DataFrame = None,
                editable: bool = True,
                min_width_cell: int = 200,
                min_row: int = 4): # if min_row 10 rows
        super().__init__(parent)
        
        self.dataframe = dataframe
        self.editable = editable
        self.min_widht_cell = min_width_cell
        self.min_row = min_row

        self.internal_frame = tk.Frame(self, height=min_height, width=max_width)
        self.internal_frame.grid(row=0, column=0, sticky='nsew')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.tree = None
        self.edit_entry = None

        self.create_style(styles.treeview_style_general_config, styles.treeview_style_header_config)
        if self.dataframe is not None:
            self.create_table()

    def set_parameter(self,
                dataframe: pd.DataFrame = None,
                editable: bool = True,
                min_width_cell: int = 200,
                min_row: int = 4):
        
        self.dataframe = dataframe
        self.editable = editable
        self.min_widht_cell = min_width_cell
        self.min_row = min_row
        self.create_table()

    def create_style(self, tsg: dict, tsh: dict): # table style
        style = ttk.Style(self)
        style.theme_use('alt')
        style.configure("Custom.Treeview", 
                        background=tsg['background'],
                        fieldbackground=tsg['fieldbackground'],
                        foreground=tsg['foreground'],
                        font=tsg['font'])
        
        style.configure("Custom.Treeview.Heading", 
                        background=tsh['header_background'],
                        foreground=tsh['header_foreground'],
                        font=tsh['font'])

        style.map("Custom.Treeview", 
                  background=[('selected', tsg['selected_bg'])],
                  foreground=[('selected', tsg['selected_fg'])])
        style.map("Custom.Treeview.Heading",
                    background=[("active", tsh['activebg'])],
                    foreground=[("active", tsh['activefg'])])
        
    def create_table(self):
        if self.tree is not None:
            self.tree.destroy()
            self.tree = None
            
        if self.edit_entry is not None:
            self.edit_entry.destroy()
            self.edit_entry = None

        self.tree = ttk.Treeview(self.internal_frame,
                                 columns=list(self.dataframe.columns),
                                 show='headings',
                                 style="Custom.Treeview",
                                 height=self.min_row)

        # Configuración de columnas
        for column in self.dataframe.columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=self.min_widht_cell)

        # Inserta filas
        for _, row in self.dataframe.iterrows():
            self.tree.insert("", "end", values=list(row))

        # Scrollbars vinculadas
        scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.tree.grid(row=0, column=0, sticky="nsew", in_=self.internal_frame)
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        #self.internal_frame.grid_rowconfigure(0, weight=1)
        self.internal_frame.grid_columnconfigure(0, weight=1)

        if self.editable:
            self.tree.bind("<Double-1>", self.on_item_double_click)
            self.edit_entry = None

    def on_item_double_click(self, event):
        item = self.tree.selection()[0]
        column = self.tree.identify_column(event.x)
        column_index = int(column.replace("#", "")) - 1
        current_value = self.tree.item(item, "values")[column_index]

        self.edit_entry = tk.Entry(self, **styles.config_entry)
        self.edit_entry.insert(0, current_value)

        self.edit_entry.bind("<Return>", lambda e: self.save_edit(item, column_index))
        self.edit_entry.bind("<FocusOut>", lambda e: self.save_edit(item, column_index))

        x, y, width, _ = self.tree.bbox(item)
        entry_width = self.tree.column(column, "width")
        self.edit_entry.place(x=self.tree.winfo_x() + (column_index * entry_width), y=self.tree.winfo_y() + y, width=entry_width)

        self.edit_entry.focus()
        self.edit_entry.select_range(0, tk.END)

    def save_edit(self, item, column_index):
        new_value = self.edit_entry.get()
        values = list(self.tree.item(item, "values"))
        values[column_index] = new_value
        self.tree.item(item, values=values)
        self.edit_entry.destroy()
        self.edit_entry = None

    def get_dataframe(self):
        data = [self.tree.item(item, "values") for item in self.tree.get_children()]
        return pd.DataFrame(data, columns=self.tree["columns"])

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x600")
    #root.maxsize(width=400, height=500)

    df1 = pd.DataFrame({
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [24, 30, 18],
        "Score": [88.5, 92.3, 79.5]
    })

    df2 = pd.DataFrame({
        "Product": ["Banana", "Watermelon", "orange"],
        "Price": [25.00, 35.75, 12.99],
        "Quantity": [100, 200, 150]
    })

    frame1 = ttk.Frame(root)
    frame1.pack(side="top", fill="x")

    frame2 = ttk.Frame(root)
    frame2.pack(side="top", fill="x")

    editable_treeview1 = EditableTreeviewGadget(parent=frame1, dataframe=df1, max_width=680)
    editable_treeview1.pack(expand=True, fill='x')

    editable_treeview2 = EditableTreeviewGadget(parent=frame2, dataframe=df2)
    editable_treeview2.pack(expand=True, fill='x')

    def on_closing():
        result_df1 = editable_treeview1.get_dataframe()
        result_df2 = editable_treeview2.get_dataframe()
        print("DataFrame 1:\n", result_df1)
        print("DataFrame 2:\n", result_df2)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
