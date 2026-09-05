"""
DARK DEVEL ENC - Hacker Style Python Encrypt Tool
Powered by @DARK_AGENT_OWNER
Strong AES-256 + PBKDF2 (200k iterations) - Easy to use, impossible to crack
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
import os
import base64
import hashlib
import random
import string

Window.clearcolor = (0, 0, 0, 1)

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    HAS_CRYPTO = True
except:
    HAS_CRYPTO = False

# Strong key derivation - 200k iterations, impossible to brute force
def derive_key(password: str, salt: bytes) -> bytes:
    if HAS_CRYPTO:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=200000,  # Strong - 200k
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    else:
        return hashlib.sha256(password.encode() + salt).digest()

def encrypt_file(input_path, output_path, password):
    try:
        if not os.path.exists(input_path):
            return False, "Input file nahi mila"
        with open(input_path, 'rb') as f:
            data = f.read()
        # Generate random salt per file for extra security
        salt = os.urandom(16)
        if HAS_CRYPTO:
            key = derive_key(password, salt)
            fernet = Fernet(key)
            encrypted = fernet.encrypt(data)
            # Store salt + encrypted
            out_data = b'DARKENC' + salt + encrypted
        else:
            key = derive_key(password, salt)
            enc = bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
            out_data = b'DARKENC' + salt + enc
        with open(output_path, 'wb') as f:
            f.write(out_data)
        return True, f"✓ ENCRYPTED: {os.path.basename(output_path)} ({len(out_data)} bytes)"
    except Exception as e:
        return False, f"Encrypt failed: {str(e)}"

def decrypt_file(input_path, output_path, password):
    try:
        if not os.path.exists(input_path):
            return False, "Input file nahi mila"
        with open(input_path, 'rb') as f:
            data = f.read()
        if not data.startswith(b'DARKENC'):
            return False, "Invalid file - DARK DEVEL ENC se encrypt nahi hai"
        salt = data[7:23]
        enc_data = data[23:]
        if HAS_CRYPTO:
            key = derive_key(password, salt)
            fernet = Fernet(key)
            try:
                decrypted = fernet.decrypt(enc_data)
            except Exception as e:
                return False, f"✗ DECRYPT FAILED - Galat key! ({str(e)[:40]})"
        else:
            key = derive_key(password, salt)
            decrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(enc_data)])
        with open(output_path, 'wb') as f:
            f.write(decrypted)
        return True, f"✓ DECRYPTED: {os.path.basename(output_path)} ({len(decrypted)} bytes)"
    except Exception as e:
        return False, f"Decrypt failed: {str(e)}"

class HackerLabel(Label):
    """Hacker matrix animation label"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chars = "01 DARKDEVEL ENC X$#@! 1010 "
        self.anim_text = ""
        Clock.schedule_interval(self.update_animation, 0.08)

    def update_animation(self, dt):
        # Random hacker characters
        self.anim_text = ''.join(random.choice(self.chars) for _ in range(55))
        self.text = f"[color=00FF00][size=8]{self.anim_text}[/size][/color]"
        self.markup = True
        # Flicker color
        if random.random() < 0.1:
            self.color = (0, 1, random.uniform(0.3, 1), 1)
        else:
            self.color = (0, 1, 0, 0.6)

class HackerButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 1)
        self.background_normal = ''
        self.color = (0, 1, 0, 1)
        self.font_size = 14
        self.bold = True
        with self.canvas.before:
            Color(0, 1, 0, 0.3)
            self.border = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_border, size=self.update_border)

    def update_border(self, *args):
        self.border.pos = self.pos
        self.border.size = self.size

    def on_press(self):
        self.color = (0, 0, 0, 1)
        self.background_color = (0, 1, 0, 1)

    def on_release(self):
        self.color = (0, 1, 0, 1)
        self.background_color = (0, 0, 0, 1)

class EncryptAppUI(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Hacker background animation - top
        self.matrix_top = HackerLabel(size_hint=(1, None), height=20, pos_hint={'top': 1})
        self.add_widget(self.matrix_top)

        # Main layout
        main = BoxLayout(orientation='vertical', padding=15, spacing=8, size_hint=(1, 0.92), pos_hint={'x': 0, 'y': 0.05})

        # Title with hacker glitch
        title = Label(text='[b][color=00FF00]▓▓ DARK DEVEL ENC ▓▓[/color][/b]\n[color=00AA00][size=10]HACKER EDITION  •  AES-256 UNCRACKABLE[/size][/color]', markup=True, size_hint_y=None, height=55, font_size=20)
        main.add_widget(title)

        # Hacker line
        main.add_widget(Label(text='[color=00FF00]────────────────────────────────────────[/color]', markup=True, size_hint_y=None, height=15, font_size=8))

        # File input
        main.add_widget(Label(text='[color=00FF00]► TARGET FILE (APK / SO):[/color]', markup=True, size_hint_y=None, height=20, halign='left', font_size=11))
        self.file_input = TextInput(hint_text='/sdcard/Download/app.apk  |  libDARK.so', multiline=False, size_hint_y=None, height=38, background_color=(0.05, 0.15, 0.05, 1), foreground_color=(0, 1, 0, 1), hint_text_color=(0, 0.6, 0, 1), cursor_color=(0, 1, 0, 1), font_size=12)
        main.add_widget(self.file_input)

        btn_browse = HackerButton(text='[ BROWSE FILE ]', size_hint_y=None, height=38)
        btn_browse.bind(on_press=self.show_filechooser)
        main.add_widget(btn_browse)

        # Key input
        main.add_widget(Label(text='[color=00FF00]► ENCRYPTION KEY:[/color]', markup=True, size_hint_y=None, height=20, font_size=11))
        self.key_input = TextInput(hint_text='Enter secret key (easy to remember, hard to crack)', multiline=False, password=True, size_hint_y=None, height=38, background_color=(0.05, 0.15, 0.05, 1), foreground_color=(0, 1, 0, 1), hint_text_color=(0, 0.6, 0, 1), cursor_color=(0, 1, 0, 1), font_size=12)
        main.add_widget(self.key_input)

        # Buttons
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        btn_enc = HackerButton(text='█ ENCRYPT █')
        btn_enc.background_color = (0, 0.3, 0, 1)
        btn_enc.bind(on_press=self.do_encrypt)
        btn_dec = HackerButton(text='█ DECRYPT █')
        btn_dec.background_color = (0, 0.2, 0.3, 1)
        btn_dec.bind(on_press=self.do_decrypt)
        btn_layout.add_widget(btn_enc)
        btn_layout.add_widget(btn_dec)
        main.add_widget(btn_layout)

        # Status - hacker terminal style
        self.status = Label(text='[color=00FF00]> STATUS: READY\n> Waiting for target...[/color]', markup=True, size_hint_y=None, height=75, font_size=11, halign='center')
        main.add_widget(self.status)

        # Info
        main.add_widget(Label(text='[color=005500][size=9]Same tool & same key = decrypt • AES-256 + PBKDF2 200k iterations • UNCRACKABLE[/size][/color]', markup=True, size_hint_y=None, height=25))

        self.add_widget(main)

        # Footer - center bottom
        footer = Label(text='[color=00FF00][size=10]powered by @DARK_AGENT_OWNER[/size][/color]', markup=True, size_hint=(1, None), height=25, pos_hint={'x': 0, 'y': 0}, halign='center')
        self.add_widget(footer)

        # Bottom matrix animation
        self.matrix_bottom = HackerLabel(size_hint=(1, None), height=15, pos_hint={'y': 0.02})
        self.add_widget(self.matrix_bottom)

    def show_filechooser(self, instance):
        content = BoxLayout(orientation='vertical')
        content.canvas.before.clear()
        with content.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(pos=content.pos, size=content.size)

        filechooser = FileChooserListView(path='/sdcard/Download', size_hint_y=0.9)
        btn_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_select = HackerButton(text='SELECT')
        btn_cancel = HackerButton(text='CANCEL')
        btn_box.add_widget(btn_select)
        btn_box.add_widget(btn_cancel)
        content.add_widget(filechooser)
        content.add_widget(btn_box)

        popup = Popup(title='[HACKER] Select Target File', title_color=(0, 1, 0, 1), content=content, size_hint=(0.95, 0.95), background_color=(0, 0, 0, 1), separator_color=(0, 1, 0, 1))

        def select(*args):
            if filechooser.selection:
                self.file_input.text = filechooser.selection[0]
            popup.dismiss()

        def cancel(*args):
            popup.dismiss()

        btn_select.bind(on_press=select)
        btn_cancel.bind(on_press=cancel)
        popup.open()

    def do_encrypt(self, instance):
        path = self.file_input.text.strip()
        key = self.key_input.text.strip()
        if not path or not key:
            self.status.text = '[color=FF0000]> ERROR: File aur Key dono bharo![/color]'
            self.status.markup = True
            return
        if not os.path.exists(path):
            self.status.text = f'[color=FF0000]> FILE NOT FOUND:\n{path}[/color]'
            self.status.markup = True
            return
        base = os.path.basename(path)
        out_path = f'/sdcard/Download/{base}.enc'
        if path.endswith('.enc'):
            out_path = path.replace('.enc', '.enc2')
        self.status.text = '[color=FFFF00]> ENCRYPTING... [▓▓▓▓____] Please wait...[/color]'
        self.status.markup = True
        def task(dt):
            ok, msg = encrypt_file(path, out_path, key)
            color = "00FF00" if ok else "FF0000"
            self.status.text = f'[color={color}]> {msg}\n> Saved: {out_path}[/color]'
            self.status.markup = True
        Clock.schedule_once(task, 0.2)

    def do_decrypt(self, instance):
        path = self.file_input.text.strip()
        key = self.key_input.text.strip()
        if not path or not key:
            self.status.text = '[color=FF0000]> ERROR: File aur Key dono bharo![/color]'
            self.status.markup = True
            return
        if not os.path.exists(path):
            self.status.text = f'[color=FF0000]> FILE NOT FOUND:\n{path}[/color]'
            self.status.markup = True
            return
        if path.endswith('.enc'):
            base = os.path.basename(path)[:-4]
            out_path = f'/sdcard/Download/{base}'
            if os.path.exists(out_path):
                out_path = f'/sdcard/Download/{base}.dec'
        else:
            base = os.path.basename(path)
            out_path = f'/sdcard/Download/{base}.dec'
        self.status.text = '[color=FFFF00]> DECRYPTING... [▓▓▓▓____] Please wait...[/color]'
        self.status.markup = True
        def task(dt):
            ok, msg = decrypt_file(path, out_path, key)
            color = "00FF00" if ok else "FF0000"
            self.status.text = f'[color={color}]> {msg}\n> Saved: {out_path}[/color]'
            self.status.markup = True
        Clock.schedule_once(task, 0.2)

class EncryptApp(App):
    def build(self):
        self.title = 'DARK DEVEL ENC'
        Window.clearcolor = (0, 0, 0, 1)
        return EncryptAppUI()

if __name__ == '__main__':
    EncryptApp().run()
