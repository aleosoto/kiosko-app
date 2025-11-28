import tkinter as tk
from app.gui import KioscoGUI

def main():
    root=tk.Tk()
    root.title("Kiosko - Autoservicio")
    KioscoGUI(root)
    root.mainloop()

if __name__=="__main__":
    main()
