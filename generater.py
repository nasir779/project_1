from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
import qrcode
import os
from kivy.utils import platform

class QRGenerator(App):
    def build(self):
        # Set window color and size
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (400, 600)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title label
        title = Label(
            text='QR Code Generator',
            font_size='24sp',
            size_hint_y=None,
            height=50,
            color=(0, 0, 0, 1)
        )
        
        # Input field with better styling
        self.input_text = TextInput(
            multiline=False,
            hint_text='Enter data for QR Code',
            size_hint_y=None,
            height=50,
            padding=(10, 10),
            background_color=(0.95, 0.95, 0.95, 1)
        )
        
        # Generate button with better styling
        generate_button = Button(
            text='Generate QR Code',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        generate_button.bind(on_press=self.generate_qr)
        
        # Status label with better styling
        self.status_label = Label(
            text='',
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30
        )
        
        # Image widget with better sizing
        self.qr_image = Image(size_hint=(1, 1))
        
        # Add widgets to layout
        layout.add_widget(title)
        layout.add_widget(self.input_text)
        layout.add_widget(generate_button)
        layout.add_widget(self.status_label)
        layout.add_widget(self.qr_image)
        
        return layout
    
    def generate_qr(self, instance):
        user_data = self.input_text.text
        if not user_data:
            self.status_label.text = 'Please enter some data'
            return
        
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(user_data)
            qr.make(fit=True)
            
            # Modified save location for Android
            if platform == 'android':
                try:
                    from android.storage import app_storage_path
                    save_dir = app_storage_path()
                    
                    # Ensure directory exists
                    qr_dir = os.path.join(save_dir, 'QRCodes')
                    if not os.path.exists(qr_dir):
                        os.makedirs(qr_dir)
                    
                    # Create unique filename
                    timestamp = int(time.time())
                    image_name = os.path.join(qr_dir, f'qrcode_{timestamp}.png')
                except:
                    image_name = 'user_qrcode.png'
            else:
                image_name = 'user_qrcode.png'
                
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(image_name)
            
            # Update image widget and status
            self.qr_image.source = image_name
            self.qr_image.reload()
            self.status_label.text = f'QR Code saved to: {image_name}'
            
        except Exception as e:
            self.status_label.text = f'Error: {str(e)}'

if __name__ == '__main__':
    QRGenerator().run()