import os
import subprocess
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.lang import Builder

Window.clearcolor = (0.039, 0.039, 0.039, 1)  # #0a0a0a

KV = '''
#:import dp kivy.metrics.dp

<RoundedButton@Button>:
    background_color: 0, 0, 0, 0
    background_normal: ''
    canvas.before:
        Color:
            rgba: (0.784, 1, 0, 1) if self.state == 'normal' else (0.831, 1, 0.149, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(4)]

<GhostButton@Button>:
    background_color: 0, 0, 0, 0
    background_normal: ''
    canvas.before:
        Color:
            rgba: (0.784, 1, 0, 0.08) if self.state == 'down' else (0, 0, 0, 0)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(4)]
        Color:
            rgba: (0.784, 1, 0, 0.3) if self.state == 'normal' else (0.784, 1, 0, 0.8)
        Line:
            rounded_rectangle: self.x, self.y, self.width, self.height, dp(4)
            width: 1.2

<MainLayout>:
    orientation: 'vertical'
    padding: dp(24)
    spacing: dp(16)

    # Header
    BoxLayout:
        size_hint_y: None
        height: dp(70)
        orientation: 'vertical'
        spacing: dp(2)

        Label:
            text: 'VOL'
            font_name: 'Roboto'
            font_size: dp(42)
            bold: True
            color: 0.784, 1, 0, 1
            size_hint_y: None
            height: dp(50)
            halign: 'left'
            text_size: self.size
            canvas.before:
                Color:
                    rgba: 0.784, 1, 0, 0.08
                Rectangle:
                    pos: self.x, self.y - dp(2)
                    size: dp(80), dp(2)

        Label:
            text: '// ajustador de volumen'
            font_size: dp(10)
            color: 0.333, 0.333, 0.333, 1
            size_hint_y: None
            height: dp(16)
            halign: 'left'
            text_size: self.size

    # File selector card
    BoxLayout:
        size_hint_y: None
        height: dp(64)
        orientation: 'vertical'
        spacing: dp(0)
        canvas.before:
            Color:
                rgba: 0.067, 0.067, 0.067, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(4)]
            Color:
                rgba: 0.784, 1, 0, 1
            Rectangle:
                pos: self.x, self.top - dp(2)
                size: dp(60), dp(2)

        BoxLayout:
            padding: dp(14), dp(10)
            spacing: dp(10)

            Label:
                id: file_label
                text: root.file_name if root.file_name else 'Ningún archivo seleccionado'
                font_size: dp(11)
                color: (0.784, 1, 0, 1) if root.file_name else (0.4, 0.4, 0.4, 1)
                halign: 'left'
                valign: 'middle'
                text_size: self.size
                shorten: True
                shorten_from: 'left'

            GhostButton:
                text: 'ELEGIR'
                font_size: dp(10)
                bold: True
                color: 0.784, 1, 0, 1
                size_hint_x: None
                width: dp(70)
                on_press: root.open_filechooser()

    # dB control
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: dp(110)
        spacing: dp(8)
        canvas.before:
            Color:
                rgba: 0.067, 0.067, 0.067, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(4)]

        BoxLayout:
            padding: dp(14), dp(12), dp(14), 0
            size_hint_y: None
            height: dp(44)

            Label:
                text: 'VOLUMEN'
                font_size: dp(9)
                color: 0.333, 0.333, 0.333, 1
                halign: 'left'
                text_size: self.size
                valign: 'middle'

            Label:
                id: db_label
                text: root.db_display
                font_size: dp(28)
                bold: True
                color: (1, 0.42, 0.21, 1) if root.db_value < -20 or root.db_value > 15 else (0.784, 1, 0, 1)
                halign: 'right'
                text_size: self.size
                valign: 'middle'

        Slider:
            id: vol_slider
            min: -30
            max: 20
            value: root.db_value
            step: 0.5
            size_hint_y: None
            height: dp(36)
            padding: dp(14)
            cursor_size: dp(20), dp(20)
            cursor_image: ''
            on_value: root.on_slider(self.value)

        # Presets
        BoxLayout:
            padding: dp(14), 0, dp(14), dp(10)
            spacing: dp(6)
            size_hint_y: None
            height: dp(30)

            GhostButton:
                text: '-10dB'
                font_size: dp(9)
                color: 0.784, 1, 0, 1
                on_press: root.set_db(-10)

            GhostButton:
                text: '0dB'
                font_size: dp(9)
                color: 0.784, 1, 0, 1
                on_press: root.set_db(0)

            GhostButton:
                text: '+5dB'
                font_size: dp(9)
                color: 0.784, 1, 0, 1
                on_press: root.set_db(5)

            GhostButton:
                text: '+10dB'
                font_size: dp(9)
                color: 0.784, 1, 0, 1
                on_press: root.set_db(10)

            GhostButton:
                text: '+20dB'
                font_size: dp(9)
                color: 0.784, 1, 0, 1
                on_press: root.set_db(20)

    # Spacer
    Widget:

    # Status / progress
    BoxLayout:
        size_hint_y: None
        height: dp(36)
        opacity: 1 if root.processing or root.status_msg else 0

        Label:
            text: root.status_msg
            font_size: dp(10)
            color: 0.4, 0.4, 0.4, 1
            halign: 'left'
            text_size: self.size
            valign: 'middle'

    ProgressBar:
        size_hint_y: None
        height: dp(3)
        max: 100
        value: root.progress
        opacity: 1 if root.processing else 0

    # Process button
    RoundedButton:
        size_hint_y: None
        height: dp(52)
        text: 'PROCESAR VIDEO'
        font_size: dp(13)
        bold: True
        color: 0, 0, 0, 1
        disabled: not root.file_name or root.processing
        on_press: root.process()

    # Download button
    GhostButton:
        size_hint_y: None
        height: dp(48)
        text: '↓  GUARDAR RESULTADO'
        font_size: dp(12)
        bold: True
        color: 0.784, 1, 0, 1
        opacity: 1 if root.output_path else 0
        disabled: not root.output_path
        on_press: root.reveal_output()

    # Note
    Label:
        size_hint_y: None
        height: dp(30)
        text: 'El archivo original no se modifica'
        font_size: dp(9)
        color: 0.25, 0.25, 0.25, 1
        halign: 'center'
        text_size: self.size
        valign: 'middle'
'''


class MainLayout(BoxLayout):
    file_name = StringProperty('')
    file_path = StringProperty('')
    db_value = NumericProperty(0)
    db_display = StringProperty('0.0 dB')
    processing = BooleanProperty(False)
    progress = NumericProperty(0)
    status_msg = StringProperty('')
    output_path = StringProperty('')

    def on_slider(self, value):
        self.db_value = round(value * 2) / 2
        sign = '+' if self.db_value > 0 else ''
        self.db_display = f'{sign}{self.db_value:.1f} dB'

    def set_db(self, val):
        self.ids.vol_slider.value = val
        self.on_slider(val)

    def open_filechooser(self):
        content = BoxLayout(orientation='vertical', spacing=dp(8), padding=dp(12))

        fc = FileChooserListView(
            path='/storage/emulated/0/',
            filters=['*.mp4', '*.mkv', '*.mov', '*.webm', '*.avi',
                     '*.mp3', '*.wav', '*.aac', '*.m4a', '*.flac'],
            dirselect=False,
        )

        btn_row = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))

        btn_cancel = Button(
            text='CANCELAR',
            font_size=dp(11),
            background_color=(0.15, 0.15, 0.15, 1),
            color=(0.6, 0.6, 0.6, 1),
        )
        btn_select = Button(
            text='SELECCIONAR',
            font_size=dp(11),
            background_color=(0.784, 1, 0, 1),
            color=(0, 0, 0, 1),
            bold=True,
        )

        content.add_widget(fc)
        content.add_widget(btn_row)
        btn_row.add_widget(btn_cancel)
        btn_row.add_widget(btn_select)

        popup = Popup(
            title='Elegir archivo',
            content=content,
            size_hint=(0.95, 0.85),
            background_color=(0.07, 0.07, 0.07, 1),
            title_color=(0.784, 1, 0, 1),
            title_size=dp(13),
            separator_color=(0.784, 1, 0, 0.4),
        )

        def select(_):
            if fc.selection:
                path = fc.selection[0]
                self.file_path = path
                self.file_name = os.path.basename(path)
                self.output_path = ''
                self.status_msg = ''
            popup.dismiss()

        btn_select.bind(on_press=select)
        btn_cancel.bind(on_press=lambda _: popup.dismiss())
        popup.open()

    def process(self):
        if not self.file_path or self.processing:
            return
        self.processing = True
        self.progress = 0
        self.output_path = ''
        self.status_msg = 'Iniciando...'
        threading.Thread(target=self._run_ffmpeg, daemon=True).start()

    def _run_ffmpeg(self):
        try:
            inp = self.file_path
            base, ext = os.path.splitext(inp)
            # Always output mp4 for video, keep original ext for audio-only
            audio_exts = {'.mp3', '.wav', '.aac', '.flac', '.m4a'}
            out_ext = ext if ext.lower() in audio_exts else '.mp4'
            db = self.db_value
            sign = '+' if db >= 0 else ''
            out = f'{base}_vol{sign}{db:.1f}dB{out_ext}'

            Clock.schedule_once(lambda dt: setattr(self, 'status_msg', 'Procesando audio...'))
            Clock.schedule_once(lambda dt: setattr(self, 'progress', 20))

            ffmpeg_bin = self._find_ffmpeg()

            cmd = [
                ffmpeg_bin,
                '-i', inp,
                '-filter:a', f'volume={db}dB',
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-y',
                out
            ]

            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            if result.returncode == 0:
                self.output_path = out
                Clock.schedule_once(lambda dt: setattr(self, 'progress', 100))
                Clock.schedule_once(lambda dt: setattr(self, 'status_msg', f'✓ Listo → {os.path.basename(out)}'))
            else:
                err = result.stderr.decode('utf-8', errors='ignore')[-200:]
                Clock.schedule_once(lambda dt: setattr(self, 'status_msg', f'Error: {err}'))
                Clock.schedule_once(lambda dt: setattr(self, 'progress', 0))

        except Exception as e:
            Clock.schedule_once(lambda dt: setattr(self, 'status_msg', f'Error: {str(e)}'))
        finally:
            Clock.schedule_once(lambda dt: setattr(self, 'processing', False))

    def _find_ffmpeg(self):
        # 1. Bundled with app (preferred)
        app_dir = os.path.dirname(os.path.abspath(__file__))
        bundled = os.path.join(app_dir, 'ffmpeg')
        if os.path.isfile(bundled):
            os.chmod(bundled, 0o755)
            return bundled
        # 2. System ffmpeg
        for path in ['/data/data/com.termux/files/usr/bin/ffmpeg', '/usr/bin/ffmpeg']:
            if os.path.isfile(path):
                return path
        return 'ffmpeg'  # last resort, rely on PATH

    def reveal_output(self):
        if not self.output_path:
            return
        out_dir = os.path.dirname(self.output_path)
        self.status_msg = f'Guardado en: {out_dir}'


class VolApp(App):
    def build(self):
        Builder.load_string(KV)
        return MainLayout()

    def on_start(self):
        from android.permissions import request_permissions, Permission  # type: ignore
        request_permissions([
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
        ])


if __name__ == '__main__':
    VolApp().run()
