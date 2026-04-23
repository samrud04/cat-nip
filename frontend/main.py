import tkinter as tk
from turtle import color

def main():
    root = tk.Tk()
    root.title("Cat-Nip")
    root.geometry("800x600")
    root.iconphoto(False, tk.PhotoImage(file="C:/Users/Dr.Satyan/Documents/Samrud/Sam Codes/cat-nip/frontend/assets/catnipico.png"))
    
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    left_frame = tk.Frame(main_frame, bg="#804000", width=450)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH)
    left_frame.pack_propagate(False)  

    right_frame = tk.Frame(main_frame, bg="#e6ccb3", width=450)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    right_frame.pack_propagate(False)

    tk.Label(left_frame, text="Cat-Nip", fg="white", bg="#804000", font=("Arial", 24)).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()