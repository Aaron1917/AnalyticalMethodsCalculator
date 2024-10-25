import tkinter as tk
from tkinter import ttk

class TabbedBrowser(tk.Frame):
    def __init__(self, parent, separator:bool = False, nav_bg ="#0091EA", selected = "#A1C8E4", active = "#0091EA"):
        super().__init__(parent)
        self.separator = separator
        
        self.list_frames = []
        self.frames = {}
        self.buttons = {}

        self.col_selected = selected
        self.col_active = active

        self.nav_frame = tk.Frame(self, bg=nav_bg)
        self.nav_frame.pack(side=tk.TOP, fill=tk.X)

        self.container = tk.Frame(self)
        self.container.pack(expand=True, fill=tk.BOTH)

    def add_tab(self, frame_class: tk.Frame, tab_name: str):

        self.list_frames.append(tab_name)

        button = tk.Button(self.nav_frame, text=tab_name, command=lambda t=tab_name: self.show_tab(t), relief="flat")
        button.pack(side=tk.LEFT)
        if self.separator:
            separator = ttk.Separator(self.nav_frame, orient="vertical")
            separator.pack(side=tk.LEFT, fill=tk.Y)

        frame = frame_class(self.container)
        self.frames[tab_name] = frame
        self.buttons[tab_name] = button
        frame.pack(fill=tk.BOTH, expand=True)

        self.show_tab(self.list_frames[0])

    def destroy_tab(self, tab_name: str):
        self.list_frames.remove(tab_name)
        self.frames[tab_name].destroy()
        self.buttons[tab_name].destroy()
        self.frames.pop(tab_name)
        self.buttons.pop(tab_name)


    def show_tab(self, frame_name):
        # Ocultar todos los frames
        for frame in self.frames.values():
            frame.pack_forget()
        for button in self.buttons.values():
            button.config(bg = self.col_active)        
        # Mostrar el frame seleccionado
        self.buttons[frame_name].config(bg=self.col_selected)
        self.frames[frame_name].pack(fill=tk.BOTH, expand=True)

class Frame1(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#A1C8E4")
        label = tk.Label(self, text="Contenido de la Pestaña 1", bg="#A1C8E4", font=("Arial", 14))
        label.pack(pady=20)

class Frame2(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#5BC0EB")
        label = tk.Label(self, text="Contenido de la Pestaña 2", bg="#5BC0EB", font=("Arial", 14))
        label.pack(pady=20)

class Frame3(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0091EA")
        label = tk.Label(self, text="Contenido de la Pestaña 3", bg="#0091EA", font=("Arial", 14))
        label.pack(pady=20)

if __name__ == "__main__":
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Custom Notebook")
    root.geometry("400x300")

    # Crear una instancia de CustomNotebook
    notebook = TabbedBrowser(root)
    notebook.pack(expand=True, fill=tk.BOTH)

    notebook.add_tab(Frame1, "Pestaña 1")
    notebook.add_tab(Frame2, "Pestaña 2")
    notebook.add_tab(Frame3, "Pestaña 3")

    # Ejecutar la aplicación
    root.mainloop()
