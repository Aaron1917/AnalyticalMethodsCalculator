import tkinter as tk
from tkinter import ttk
import pandas as pd
import styles

class EditableTreeviewGadget(tk.Frame):
    def __init__(self, parent,
                width=400,
                height=300,
                bg =  '#E0F7FA',
                dataframe: pd.DataFrame = None,
                editable: bool = True,
                min_width_cell: int = 200,
                num_visible_rows: int = None,
                color_row:list = None):
        super().__init__(parent, width=width, height=height, bg=bg)
        
        self.dataframe = dataframe
        self.editable = editable
        self.min_widht_cell = min_width_cell
        self.num_visible_rows = num_visible_rows if num_visible_rows else 4
        self.color_row = color_row.copy() if color_row else styles.treeview_style_general_config['rows_bg'] #["#E0F7FA", "#81D4FA"]

        self.internal_frame = tk.Frame(self, bg=bg)
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
                editable: bool = None,
                min_width_cell: int = None,
                num_visible_rows: int = None):
        
        self.dataframe = dataframe if dataframe is not None else self.dataframe
        self.editable = editable if editable is not None else self.editable
        self.min_widht_cell = min_width_cell if min_width_cell is not None else self.min_widht_cell
        self.num_visible_rows = num_visible_rows if num_visible_rows is not None else self.num_visible_rows
        if self.dataframe is not None:
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
                                 selectmode="browse",
                                 height=self.num_visible_rows)

        # Configuración de columnas
        for column in self.dataframe.columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=self.min_widht_cell)

        # Inserta filas
        last_value = None
        row_color = 0  # 0 para color1, 1 para color2
        col1 = self.dataframe.columns.to_list()[0]
        for _, row in self.dataframe.iterrows():
            current_value = row[col1]
            if current_value != last_value:
                row_color = 1 - row_color
                last_value = current_value

            # Asignar color según el estado
            if row_color == 0:
                self.tree.insert("", "end", values=list(row), tags=('color1',))
            else:
                self.tree.insert("", "end", values=list(row), tags=('color2',))
        
        self.tree.tag_configure('color1', background=self.color_row[0])
        self.tree.tag_configure('color2', background=self.color_row[1])

        # Scrollbars vinculadas
        scrollbar_y = ttk.Scrollbar(self.internal_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(self.internal_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.tree.grid(row=0, column=0, sticky='new')
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        self.internal_frame.grid_rowconfigure(0, weight=1)
        self.internal_frame.grid_rowconfigure(1, weight=0)
        self.internal_frame.grid_columnconfigure(0, weight=1)
        self.internal_frame.grid_columnconfigure(1, weight=0)

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
    root.geometry("400x600+50+50")
    root.minsize(width=400, height=600)

    df1 = pd.DataFrame({
        "Name": ["Alice", "Bob", "Charlie", "Edward", "Marcus", "Dom", "John"],
        "Age": [24, 30, 18, 15, 23, 22, 19],
        "Score": [88.5, 92.3, 79.5, 89.1, 75.3, 79.5, 91.4]
    })

    df2 = pd.DataFrame({
        "Product": ["Banana", "Watermelon", "orange"],
        "Price": [25.00, 35.75, 12.99],
        "Quantity": [100, 200, 150]
    })
    
    main_frame = tk.Frame(root, bg='pink')
    main_frame.pack(fill='both', expand=1)

    frame1 = tk.Frame(main_frame)
    frame2 = tk.Frame(main_frame)
    frame1.grid(row=1, column=0, sticky='nsew')
    frame2.grid(row=0, column=0, sticky='nsew')
    main_frame.grid_rowconfigure(0, weight=0, minsize=300)
    main_frame.grid_rowconfigure(1, weight=0, minsize=200)
    main_frame.grid_columnconfigure(0, weight=1)

    editable_treeview1 = EditableTreeviewGadget(frame1, width=400, height=20, bg='green', dataframe=df1)
    editable_treeview1.pack(fill='both', expand=1)

    editable_treeview2 = EditableTreeviewGadget(parent=frame2, dataframe=df2)
    editable_treeview2.pack(fill='both', expand=1)

    def on_closing():
        result_df1 = editable_treeview1.get_dataframe()
        result_df2 = editable_treeview2.get_dataframe()
        print("DataFrame 1:\n", result_df1)
        print("DataFrame 2:\n", result_df2)
        root.destroy()

    #root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
