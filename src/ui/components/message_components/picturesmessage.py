from kivy.lang.builder import Builder
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.image import Image
from PIL import Image as PILImage
import os
import tkinter as tk
from tkinter import filedialog
import io
import base64

Builder.load_string(
    """
<PicturesMessage>:
    elevation: 2
    md_bg_color: app.theme_cls.bg_light
    orientation: "vertical"
    size_hint_y: None
    height: self.minimum_height
    padding: "20dp", "20dp", "20dp", "20dp"
    spacing: "8dp"

    RelativeLayout:
        size_hint_y: None
        size_hint_x: 1
        height: "40dp"
        Label:
            text: "Pictures Message"
            color: app.theme_cls.primary_color
            font_size: "22sp"
            bold: True
            size_hint_y: None
            height: self.texture_size[1]
            pos_hint: {"center_y": 0.5, "center_x": .15}
        MDIcon:
            icon: "image"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            size_hint_x: None
            width: self.texture_size[1]
            pos_hint: {"center_y": 0.5, "left": 1}

        MDIconButton:
            icon: "trash-can-outline"
            pos_hint: {"center_y": 0.5, "right": 1}
            on_release: root.parent.remove_widget(root)

    BoxLayout:
        orientation: "vertical"
        size_hint_y: None
        height: "200dp"
        spacing: "8dp"

        Image:
            id: image_preview
            size_hint_y: None
            height: "120dp"
            source: ""
            allow_stretch: True
            keep_ratio: True

        MDRaisedButton:
            text: "Browse Image"
            size_hint_y: None
            height: "48dp"
            on_release: root.show_file_chooser()
    """
)


class PicturesMessage(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create a hidden root window for tkinter
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window
        self.image_data = None

    def show_file_chooser(self):
        """Shows the native file chooser dialog to select an image"""
        # Define file types
        filetypes = (
            ('Image files', '*.png *.jpg *.jpeg *.gif *.bmp'),
            ('All files', '*.*')
        )
        
        # Open the native file dialog
        filename = filedialog.askopenfilename(
            title='Select an image',
            initialdir=os.path.expanduser("~"),
            filetypes=filetypes
        )
        
        if filename:
            try:
                # Load and process the image
                with PILImage.open(filename) as img:
                    # Convert to RGB if necessary (for PNG with transparency)
                    if img.mode in ('RGBA', 'LA'):
                        background = PILImage.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1])
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Resize if too large (max 1000px on longest side)
                    max_size = 1000
                    if max(img.size) > max_size:
                        ratio = max_size / max(img.size)
                        new_size = tuple(int(dim * ratio) for dim in img.size)
                        img = img.resize(new_size, PILImage.Resampling.LANCZOS)
                    
                    # Save to bytes buffer
                    buffer = io.BytesIO()
                    img.save(buffer, format='JPEG', quality=85)
                    self.image_data = buffer.getvalue()
                    
                    # Create a temporary file for preview
                    temp_path = os.path.join(os.path.dirname(filename), 'temp_preview.jpg')
                    img.save(temp_path, 'JPEG')
                    self.ids.image_preview.source = temp_path
                    
            except Exception as e:
                print(f"Error processing image: {e}")
                self.image_data = None
                self.ids.image_preview.source = ""

    def get_image_data(self):
        """Returns the processed image data for sending"""
        return self.image_data

    def __del__(self):
        """Clean up tkinter root window and temporary files when the widget is destroyed"""
        if hasattr(self, 'root'):
            self.root.destroy()
        
        # Clean up temporary preview file
        if hasattr(self, 'ids') and self.ids.image_preview.source:
            try:
                os.remove(self.ids.image_preview.source)
            except:
                pass 