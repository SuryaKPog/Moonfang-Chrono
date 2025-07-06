import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk, ImageDraw
import time
import datetime
import os
\
class WolfClock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        
        # Widget size (3:4 ratio)
        self.width = 180
        self.height = 240
        self.corner_radius = 20
        self.border_width = 2
        
        self.time_font_size = 12  # Change this number
        self.date_font_size = 7  # Change this number
        
        # Setup window
        self.root.geometry(f"{self.width}x{self.height}+100+100")
        self.root.wm_attributes("-transparentcolor", "gray2")
        self.canvas = tk.Canvas(self.root, 
                              width=self.width, 
                              height=self.height, 
                              bg='gray2',
                              highlightthickness=0)
        self.canvas.pack()
        
        # Initialize fonts
        self.initialize_fonts()
        
        # Load backgrounds
        self.backgrounds = {
            "dawn": self.process_image("Rectangle 1.png"),
            "day": self.process_image("Rectangle 2.png"),
            "dusk": self.process_image("Rectangle 3.png"),
            "night": self.process_image("Rectangle 4.png")
        }
        
        # Mouse controls
        self.canvas.bind("<Button-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.on_move)
        self.canvas.bind("<Button-3>", lambda e: self.root.destroy())
        
        self.update_clock()
    
    def initialize_fonts(self):
        """Initialize fonts with adjustable sizes"""
        system_fonts = list(font.families())
        
        # List of preferred fonts in order of priority
        preferred_fonts = [
            "Press Start 2P",  # First choice
            "VT323",           # Alternative pixel font
            "Courier New",     # Common monospace
            "Courier"          # Fallback
        ]
        
        # Find first available font
        for font_name in preferred_fonts:
            if font_name in system_fonts:
                self.time_font = font.Font(family=font_name, size=self.time_font_size)
                self.date_font = font.Font(family=font_name, size=self.date_font_size)
                print(f"Using font: {font_name} (Time: {self.time_font_size}px, Date: {self.date_font_size}px)")
                return
        
        # Ultimate fallback
        self.time_font = font.Font(size=self.time_font_size, weight="bold")
        self.date_font = font.Font(size=self.date_font_size)
        print("Using default system font")

    def process_image(self, filename):
        """Adds border and rounded corners to the image"""
        try:
            img = Image.open(filename).convert("RGBA")
            img = img.resize((self.width, self.height), Image.NEAREST)
            
            # Create main image
            main_img = Image.new("RGBA", (self.width, self.height), (0,0,0,0))
            draw = ImageDraw.Draw(main_img)
            
            # Draw white border
            draw.rounded_rectangle(
                [0, 0, self.width-1, self.height-1],
                radius=self.corner_radius,
                outline="white",
                width=self.border_width
            )
            
            # Apply rounded corners
            mask = Image.new('L', (self.width, self.height), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.rounded_rectangle(
                [self.border_width, self.border_width,
                 self.width-self.border_width,
                 self.height-self.border_width],
                radius=self.corner_radius-self.border_width,
                fill=255
            )
            img.putalpha(mask)
            main_img.alpha_composite(img)
            
            return ImageTk.PhotoImage(main_img)
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            blank = Image.new('RGBA', (self.width, self.height), (0,0,0,0))
            return ImageTk.PhotoImage(blank)

    def get_time_of_day(self):
        hour = datetime.datetime.now().hour
        if 5 <= hour < 10: return "dawn"
        elif 10 <= hour < 16: return "day"
        elif 16 <= hour < 20: return "dusk"
        else: return "night"

    def start_move(self, event):
        self._offset = (event.x, event.y)

    def on_move(self, event):
        x = self.root.winfo_x() + event.x - self._offset[0]
        y = self.root.winfo_y() + event.y - self._offset[1]
        self.root.geometry(f"+{x}+{y}")

    def update_clock(self):
        self.canvas.delete("all")
        
        # Draw background
        time_of_day = self.get_time_of_day()
        self.canvas.create_image(0, 0, 
                               image=self.backgrounds[time_of_day], 
                               anchor="nw")
        
        # Draw text
        self.canvas.create_text(15, 15,
                              text=time.strftime("%H:%M:%S"),
                              font=self.time_font,
                              fill="#FDFFBD",
                              anchor="nw")
        
        self.canvas.create_text(15, 40,
                              text=time.strftime("%a %d %b"),
                              font=self.date_font,
                              fill="white",
                              anchor="nw")
        
        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    # Check for required files
    required_files = [f"Rectangle {i}.png" for i in range(1,5)]
    missing = [f for f in required_files if not os.path.exists(f)]
    
    if missing:
        print("Missing image files:", ", ".join(missing))
    else:
        clock = WolfClock()
        clock.root.mainloop()
