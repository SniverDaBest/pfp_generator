import hashlib

class Pattern:
    def __init__(self, data: list | tuple, bgcolor: str, fgcolor: str):
        self.data = data
        self.bgcolor = bgcolor
        self.fgcolor = fgcolor

class ProfilePicture:
    def __init__(self, username, width, height):
        self.username = username
        self.width = width
        self.height = height

    def generate(self):
        print(f"Username is {hashlib.sha256(self.username.encode()).hexdigest()}")
        bgcolor = '#' + hashlib.sha256(self.username.encode()).hexdigest()[:6]
        fgcolor = '#' + hashlib.sha256(bgcolor.encode()).hexdigest()[7:13]

        pattern = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                idx = (y * self.width + x) % len(hashlib.sha256(bgcolor.encode()).hexdigest())
                if hashlib.sha256(bgcolor.encode()).hexdigest()[idx] in 'acef13579':
                    row.append('#')
                else:
                    row.append(' ')
            pattern.append(''.join(row))

        return Pattern(pattern, bgcolor, fgcolor)

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import ttk, filedialog
    from PIL import Image, ImageDraw
    import os
    
    def draw_profile_picture(canvas, pattern, width, height):
        canvas.delete("all")
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        scale_x = canvas_width / width
        scale_y = canvas_height / height

        for x in range(width):
            for y in range(height):
                color = pattern.fgcolor if pattern.data[y][x] == ' ' else pattern.bgcolor
                canvas.create_rectangle(x * scale_x, y * scale_y, (x + 1) * scale_x, (y + 1) * scale_y, fill=color, outline=color)

    def update_profile_picture(canvas, username, width, height):
        profile_picture = ProfilePicture(username.get(), int(width.get()), int(height.get()))
        pattern = profile_picture.generate()
        draw_profile_picture(canvas, pattern, int(width.get()), int(height.get()))

    def export_image(canvas):
        canvas.update()
        canvas.postscript(file="temp.ps", colormode='color', x=0, y=0, width=canvas.winfo_width(), height=canvas.winfo_height())

        filename = filedialog.asksaveasfilename(filetypes=[("PNG file", "*.png"), ("Bitmap file", "*.bmp"), ("GIF file", "*.gif"), ("TIFF file", "*.tiff"), ("Postscript file", "*.ps"), ("All files", "*.*")])

        if filename:
            file_extension = os.path.splitext(filename)[1]
            print(f"Selected file extension: {file_extension}")

            if file_extension == ".ps":
                os.rename("temp.ps", filename)
                return

            img = Image.open("temp.ps")
            img.save(filename, file_extension[1:])
            img.close()
            os.remove("temp.ps")

    def main():
        root = tk.Tk()
        root.geometry("500x530")
        root.title("PFP Generator GUI")

        canvas = tk.Canvas(root, width=400, height=400)
        canvas.pack(fill=tk.BOTH, expand=True)

        controls_frame = ttk.Frame(root)
        controls_frame.pack(fill=tk.X, side=tk.BOTTOM)

        tk.Label(controls_frame, text="Username:").pack(side=tk.LEFT)
        username = tk.StringVar()
        username_entry = ttk.Entry(controls_frame, textvariable=username, width=16)
        username_entry.pack(side=tk.LEFT)

        ttk.Separator(controls_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=7)

        tk.Label(controls_frame, text="Width:").pack(side=tk.LEFT)
        width = tk.StringVar(value="8")
        width_entry = ttk.Entry(controls_frame, textvariable=width, width=2)
        width_entry.pack(side=tk.LEFT)

        ttk.Separator(controls_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=7)

        tk.Label(controls_frame, text="Height:").pack(side=tk.LEFT)
        height = tk.StringVar(value="8")
        height_entry = ttk.Entry(controls_frame, textvariable=height, width=2)
        height_entry.pack(side=tk.LEFT)
        
        ttk.Separator(controls_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=7)

        export_button = ttk.Button(controls_frame, text="Export", command=lambda: export_image(canvas))
        export_button.pack(side=tk.LEFT)

        def on_change(*args):
            update_profile_picture(canvas, username, width, height)

        username.trace_add("write", on_change)
        width.trace_add("write", on_change)
        height.trace_add("write", on_change)

        root.mainloop()

    main()