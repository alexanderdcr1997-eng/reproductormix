import os
import threading
from kivy.lang import Builder
from kivy.core.audio import SoundLoader
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
import yt_dlp

# --- DISEÑO TÉCNICO Y FUNCIONAL ---
KV = '''
MDBoxLayout:
    orientation: 'vertical'

    MDBottomNavigation:
        panel_color: 0.1, 0.1, 0.1, 1
        text_color_active: 0.2, 0.7, 1, 1

        # --- PESTAÑA 1: BIBLIOTECA Y REPRODUCTOR ---
        MDBottomNavigationItem:
            name: 'screen_library'
            text: 'Biblioteca'
            icon: 'music-box-multiple'

            MDBoxLayout:
                orientation: 'vertical'
                md_bg_color: 0.05, 0.05, 0.05, 1

                # Cabecera con Botón de Carpeta
                MDBoxLayout:
                    size_hint_y: None
                    height: dp(70)
                    padding: dp(15)
                    spacing: dp(15)
                    md_bg_color: 0.15, 0.15, 0.15, 1

                    MDIconButton:
                        icon: "folder-music"
                        theme_text_color: "Custom"
                        text_color: 0.2, 0.7, 1, 1
                        on_release: app.file_manager_open()
                    
                    MDLabel:
                        id: current_folder_label
                        text: "Toca la carpeta para buscar música -->"
                        color: 1, 1, 1, 0.7
                        valign: "center"
                        shorten: True
                        shorten_from: 'right'

                # Lista de Canciones (Scrollable)
                RecycleView:
                    id: rv_music
                    viewclass: 'SongItem'
                    RecycleBoxLayout:
                        default_size: None, dp(56)
                        default_size_hint: 1, None
                        size_hint_y: None
                        height: self.minimum_height
                        orientation: 'vertical'

                # --- MINIREPRODUCTOR INFERIOR ---
                MDBoxLayout:
                    size_hint_y: None
                    height: dp(90)
                    padding: dp(10)
                    md_bg_color: 0.12, 0.12, 0.12, 1
                    
                    # Info Canción Actual
                    MDBoxLayout:
                        orientation: 'vertical'
                        size_hint_x: 0.5
                        padding: [10, 0, 0, 0]
                        MDLabel:
                            id: player_title
                            text: "DALEMIX Player"
                            bold: True
                            color: 1, 1, 1, 1
                            shorten: True
                        MDLabel:
                            id: player_artist
                            text: "Selecciona una carpeta"
                            font_style: "Caption"
                            color: 0.7, 0.7, 0.7, 1

                    # Controles
                    MDIconButton:
                        icon: "skip-previous"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        on_release: app.play_previous()
                    
                    MDIconButton:
                        id: btn_play
                        icon: "play-circle"
                        icon_size: "48sp"
                        theme_text_color: "Custom"
                        text_color: 0.2, 0.7, 1, 1
                        on_release: app.play_pause()
                    
                    MDIconButton:
                        icon: "skip-next"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        on_release: app.play_next()

        # --- PESTAÑA 2: DESCARGADOR ---
        MDBottomNavigationItem:
            name: 'screen_download'
            text: 'Descargar'
            icon: 'download'

            MDScreen:
                md_bg_color: 0.05, 0.05, 0.05, 1
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: dp(30)
                    spacing: dp(20)
                    pos_hint: {"center_y": .6}

                    MDLabel:
                        text: "Descargador Universal"
                        halign: "center"
                        font_style: "H5"
                        color: 1, 1, 1, 1
                    
                    MDTextField:
                        id: link_input
                        hint_text: "Pega el enlace aquí"
                        helper_text: "Soporta YouTube y otros"
                        color_mode: 'custom'
                        line_color_focus: 0.2, 0.7, 1, 1
                        current_hint_text_color: 0.5, 0.5, 0.5, 1
                        text_color_normal: 1, 1, 1, 1

                    MDRaisedButton:
                        text: "DESCARGAR AUDIO"
                        pos_hint: {"center_x": .5}
                        md_bg_color: 0.2, 0.7, 1, 1
                        text_color: 0, 0, 0, 1
                        on_release: app.start_download()
                    
                    MDLabel:
                        id: download_status
                        text: ""
                        halign: "center"
                        theme_text_color: "Error"
                    
                    Widget:

<SongItem>:
    text: root.text
    theme_text_color: "Custom"
    text_color: 1, 1, 1, 1
    bg_color: 0.05, 0.05, 0.05, 1
    on_release: app.play_from_list(root.filepath, root.index)
    IconLeftWidget:
        icon: "music-note"
        theme_text_color: "Custom"
        text_color: 0.2, 0.7, 1, 1
'''

class SongItem(OneLineIconListItem):
    filepath = ""
    index = 0

class DaleMixApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.music_list = []
        self.current_index = -1
        self.sound = None
        self.is_playing = False
        
        # Configuración del Gestor de Archivos
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=False,
            ext=['.mp3', '.m4a', '.wav', '.ogg']
        )
        
        # Permisos al iniciar
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE, 
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_MEDIA_AUDIO
            ])
            
        return Builder.load_string(KV)

    # --- GESTOR DE ARCHIVOS ---
    def file_manager_open(self):
        # Ruta inicial segura para Android
        initial_path = '/storage/emulated/0/'
        self.file_manager.show(initial_path)

    def select_path(self, path):
        self.exit_manager()
        toast(f"Cargando carpeta...")
        
        # Si eligió una carpeta, buscar música dentro
        if os.path.isdir(path):
            self.scan_folder(path)
        else:
            # Si eligió un archivo, cargar la carpeta de ese archivo
            self.scan_folder(os.path.dirname(path))

    def exit_manager(self, *args):
        self.file_manager.close()

    def scan_folder(self, folder_path):
        self.music_list = []
        data_for_list = []
        
        self.root.ids.current_folder_label.text = os.path.basename(folder_path)
        
        try:
            for file in os.listdir(folder_path):
                if file.lower().endswith(('.mp3', '.m4a', '.wav')):
                    full_path = os.path.join(folder_path, file)
                    self.music_list.append(full_path)
                    
                    # Añadir a la lista visual
                    data_for_list.append({
                        "text": file,
                        "filepath": full_path,
                        "index": len(self.music_list) - 1
                    })
            
            self.root.ids.rv_music.data = data_for_list
            toast(f"Se encontraron {len(self.music_list)} canciones")
            
        except Exception as e:
            toast("Error leyendo carpeta (¿Permisos?)")
            print(e)

    # --- REPRODUCTOR ---
    def play_from_list(self, filepath, index):
        self.current_index = index
        self.load_song(filepath)

    def load_song(self, filepath):
        if self.sound:
            self.sound.stop()
        
        try:
            self.sound = SoundLoader.load(filepath)
            if self.sound:
                self.sound.play()
                self.is_playing = True
                self.root.ids.btn_play.icon = "pause-circle"
                self.root.ids.player_title.text = os.path.basename(filepath)
                self.root.ids.player_artist.text = "Reproduciendo..."
                
                # Configurar siguiente automático
                self.sound.bind(on_stop=self.on_song_finish)
            else:
                toast("No se pudo reproducir este archivo")
        except:
            toast("Error de audio")

    def play_pause(self):
        if not self.sound: return
        if self.is_playing:
            self.sound.stop()
            self.root.ids.btn_play.icon = "play-circle"
            self.is_playing = False
        else:
            self.sound.play()
            self.root.ids.btn_play.icon = "pause-circle"
            self.is_playing = True

    def play_next(self):
        if not self.music_list: return
        next_idx = (self.current_index + 1) % len(self.music_list)
        self.play_from_list(self.music_list[next_idx], next_idx)

    def play_previous(self):
        if not self.music_list: return
        prev_idx = (self.current_index - 1) % len(self.music_list)
        self.play_from_list(self.music_list[prev_idx], prev_idx)

    def on_song_finish(self, dt):
        self.play_next()

    # --- DESCARGADOR CORREGIDO ---
    def start_download(self):
        url = self.root.ids.link_input.text
        if not url: return
        
        self.root.ids.download_status.text = "Iniciando descarga..."
        threading.Thread(target=self.download_thread, args=(url,)).start()

    def download_thread(self, url):
        # Guardar en carpeta Music pública
        path = '/storage/emulated/0/Music' if platform == 'android' else '.'
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'ignoreerrors': True,
            'nocheckcertificate': True,
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Actualizar UI en hilo principal
            self.update_status("¡Descarga Exitosa! Búscalo en la carpeta Music")
        except Exception as e:
            self.update_status(f"Error: {str(e)}")

    def update_status(self, msg):
        # Pequeño truco para actualizar texto desde otro hilo
        self.root.ids.download_status.text = msg
        toast(msg)

if __name__ == '__main__':
    DaleMixApp().run()