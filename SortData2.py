import tkinter
from pathlib import Path

dirs = {".png": "Images",
        ".jpeg": "Images",
        ".jpg": "Images",
        ".gif": "Images",
        ".mp4": "Videos",
        ".mov": "Videos",
        ".zip": "Archives",
        ".pdf": "Documents",
        ".txt": "Documents",
        ".json": "Documents",
        ".mp3": "Music",
        ".wav": "Music"}

window = tkinter.Tk()
window.title("file sorter")
window.minsize(width=300, height=300)
window.maxsize(width=300, height=500)


# Label
my_label = tkinter.Label(text="Enter the path", font=("Arial", 20, "bold"))
my_label.pack(padx=5, pady=10)


# Button
def clicked():
    sort_dir = Path(input.get())  # creation of the path

    # lists all the elements contained in our file
    file = [f for f in sort_dir.iterdir() if f.is_file()]
    for f in file:
        output_dir = sort_dir / dirs.get(f.suffix, "Other")
        output_dir.mkdir(exist_ok=True)
        f.rename(output_dir / f.name)


button = tkinter.Button(window, height=1, width=10, text="sorted", command=clicked)
button.pack(padx=5,pady=10, side=tkinter.BOTTOM)

# Entry
input = tkinter.Entry(window, width=30)
input.pack(padx=5,pady=10)


window.mainloop()
