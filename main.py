import os
import random
import threading
from kivy.lang import Builder
from kivy.core.audio import SoundLoader
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.toast import toast
import yt_dlp

# --- DISEÑO DE INTERFAZ (DALEMIX STYLE) ---
KV = '''
MDBoxLayout:
    orientation: 'vertical'

    MDBottomNavigation:
        # Color del panel de pestañas (Gris oscuro elegante)
        panel_color: 0.15, 0.15, 0.15, 1
        selected_color_background: 0, 0, 0, 0
        text_color_active: 1, 1, 1, 1
        text_color_normal: 0.5, 0.5, 0.5, 1

        # --- PESTAÑA 1: REPRODUCTOR ---
        MDBottomNavigationItem:
            name: 'screen_player'
            text: 'Reproductor'
            icon: 'music-circle'

            MDScreen:
                md_bg_color: 0.1, 0.1, 0.1, 1  # Fondo casi negro (Monocromático)

                # Cabecera simple
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: dp(20)
                    spacing: dp(20)

                    # Barra Superior (Simulada como la imagen)
                    MDBoxLayout:
                        adaptive_height: True
                        MDIconButton:
                            icon: "chevron-down"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1
                        MDLabel:
                            text: "AHORA REPRODUCIENDO"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 0.7, 0.7, 0.7, 1
                            font_style: "Caption"
                        MDIconButton:
                            icon: "cog-outline" # Configuración
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1

                    # Carátula / Visualizador (El cuadro grande central)
                    MDCard:
                        size_hint: None, None
                        size: dp(280), dp(280)
                        pos_hint: {"center_x": .5}
                        radius: [30,]
                        md_bg_color: 0.2, 0.2, 0.2, 1
                        elevation: 2
                        
                        MDRelativeLayout:
                            MDIcon:
                                icon: "music-note-eighth"
                                font_size: "100sp"
                                pos_hint: {"center_x": .5, "center_y": .5}
                                theme_text_color: "Custom"
                                text_color: 0.5, 0.5, 0.5, 1
                            
                            # Aquí iría la onda de sonido (imagen estática por ahora)
                            MDLabel:
                                text: "DALEMIX"
                                halign: "center"
                                pos_hint: {"center_y": .2}
                                theme_text_color: "Custom"
                                text_color: 1, 1, 1, 0.3
                                font_style: "H3"

                    # Info de la Canción
                    MDBoxLayout:
                        orientation: "vertical"
                        adaptive_height: True
                        spacing: dp(5)
                        MDLabel:
                            id: song_title
                            text: "Selecciona una canción"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1
                            font_style: "H5"
                            bold: True
                        MDLabel:
                            id: song_artist
                            text: "Artista Desconocido"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 0.6, 0.6, 0.6, 1
                            font_style: "Subtitle1"

                    # Barra de Progreso (Visual)
                    MDSlider:
                        min: 0
                        max: 100
                        value: 0
                        color: 1, 1, 1, 1
                        thumb_color_active: 1, 1, 1, 1
                        thumb_color_inactive: 0.5, 0.5, 0.5, 1

                    # Controles de Reproducción (Estilo Imagen)
                    MDBoxLayout:
                        adaptive_height: True
                        spacing: dp(15)
                        pos_hint: {"center_x": .5}
                        
                        MDIconButton:
                            icon: "shuffle"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1
                            on_release: app.toggle_shuffle()
                            id: btn_shuffle
                        
                        MDIconButton:
                            icon: "skip-previous"
                            icon_size: "35sp"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1
                            on_release: app.play_previous()

                        # Botón Play Grande
                        MDIconButton:
                            id: play_btn
                            icon: "play-circle-outline"
                            icon_size: "70sp"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1
                            on_release: app.play_pause()

                        MDIconButton:
                            icon: "skip-next"
                            icon_size: "35sp"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1
                            on_release: app.play_next()

                        MDIconButton:
                            icon: "repeat"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1

                    # Pie de página (Volumen y Favoritos)
                    MDBoxLayout:
                        adaptive_height: True
                        padding: [dp(20), 0, dp(20), 0]
                        MDIconButton:
                            icon: "volume-high"
                            theme_text_color: "Custom"
                            text_color: 0.6, 0.6, 0.6, 1
                        Widget:
                        MDIconButton:
                            icon: "heart-outline"
                            theme_text_color: "Custom"
                            text_color: 0.6, 0.6, 0.6, 1


        # --- PESTAÑA 2: DESCARGADOR ---
        MDBottomNavigationItem:
            name: 'screen_download'
            text: 'Descargas'
            icon: 'download-circle'

            MDScreen:
                md_bg_color: 0.1, 0.1, 0.1, 1
                
                MDCard:
                    orientation: "vertical"
                    size_hint: 0.9, None
                    height: dp(200)
                    pos_hint: {"center_x": .5, "center_y": .5}
                    padding: 20
                    radius: [20,]
                    md_bg_color: 0.15, 0.15, 0.15, 1
                    elevation: 3

                    MDLabel:
                        text: "YouTube a MP3"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        font_style: "H6"
                    
                    MDTextField:
                        id: link_input
                        hint_text: "Pegar enlace aquí"
                        text_color_normal: 1, 1, 1, 1
                        text_color_focus: 1, 1, 1, 1
                        line_color_focus: 1, 1, 1, 1
                        hint_text_color_normal: 0.5, 0.5, 0.5, 1
                        mode: "rectangle"

                    Widget:
                        size_hint_y: None
                        height: dp(20)

                    MDRaisedButton:
                        text: "DESCARGAR AHORA"
                        pos_hint: {"center_x": .5}
                        md_bg_color: 1, 1, 1, 0.2 # Botón translúcido elegante
                        text_color: 1, 1, 1, 1
                        on_release: app.start_download_thread()
'''

class DaleMixApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        self.music_list = []
        self.current_index = 0
        self.sound = None
        self.is_playing = False
        self.is_shuffle = False
        
        # --- PERMISOS ANDROID (Crucial para leer música) ---
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE, 
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_MEDIA_AUDIO # Necesario en Android nuevos (13+)
            ])

        return Builder.load_string(KV)

    def on_start(self):
        # Escanear música al iniciar
        self.scan_music()

    def scan_music(self):
        self.music_list = []
        # Rutas típicas donde Android guarda música
        search_paths = [
            '/storage/emulated/0/Music', 
            '/storage/emulated/0/Download', 
            '/storage/emulated/0/WhatsApp/Media/WhatsApp Audio',
            '.' # Para probar en PC
        ]
        
        for path in search_paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.lower().endswith('.mp3'):
                            self.music_list.append(os.path.join(root, file))
        
        if self.music_list:
            toast(f"¡DALEMIX cargó {len(self.music_list)} canciones!")
            self.update_song_info(0)
        else:
            self.root.ids.song_title.text = "Sin MP3 encontrados"

    def update_song_info(self, index):
        if not self.music_list: return
        path = self.music_list[index]
        filename = os.path.basename(path).replace('.mp3', '')
        
        # Intentamos separar Artista - Cancion si el archivo tiene guión
        if '-' in filename:
            parts = filename.split('-', 1)
            self.root.ids.song_artist.text = parts[0].strip()
            self.root.ids.song_title.text = parts[1].strip()
        else:
            self.root.ids.song_artist.text = "Desconocido / Local"
            self.root.ids.song_title.text = filename

    def play_song(self, index):
        if not self.music_list: return

        if self.sound:
            self.sound.stop()

        self.current_index = index
        self.update_song_info(index)
        
        source = self.music_list[index]
        self.sound = SoundLoader.load(source)
        
        if self.sound:
            self.sound.play()
            self.root.ids.play_btn.icon = "pause-circle-outline"
            self.is_playing = True
            self.sound.bind(on_stop=self.on_song_finish)

    def play_pause(self):
        if not self.sound:
            self.play_song(self.current_index)
            return

        if self.is_playing:
            self.sound.stop()
            self.root.ids.play_btn.icon = "play-circle-outline"
            self.is_playing = False
        else:
            self.sound.play()
            self.root.ids.play_btn.icon = "pause-circle-outline"
            self.is_playing = True

    def play_next(self):
        if not self.music_list: return
        if self.is_shuffle:
            next_index = random.randint(0, len(self.music_list) - 1)
        else:
            next_index = (self.current_index + 1) % len(self.music_list)
        self.play_song(next_index)

    def play_previous(self):
        if not self.music_list: return
        prev_index = (self.current_index - 1) % len(self.music_list)
        self.play_song(prev_index)

    def toggle_shuffle(self):
        self.is_shuffle = not self.is_shuffle
        color = (0.2, 0.8, 0.2, 1) if self.is_shuffle else (1, 1, 1, 1) # Verde si está activo
        self.root.ids.btn_shuffle.text_color = color
        toast("Modo Aleatorio: " + ("ON" if self.is_shuffle else "OFF"))

    def on_song_finish(self, dt):
        self.play_next()

    # --- LÓGICA DE DESCARGAS ---
    def start_download_thread(self):
        url = self.root.ids.link_input.text
        if not url:
            toast("¡Falta el link!")
            return
        
        toast("Descargando... (Esto puede tardar)")
        threading.Thread(target=self.download_audio, args=(url,)).start()

    def download_audio(self, url):
        path_to_save = '/storage/emulated/0/Music' if platform == 'android' else '.'
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{path_to_save}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            toast("¡Descargado en Música!")
            self.scan_music() 
        except Exception as e:
            toast("Error en la descarga")

if __name__ == '__main__':
    DaleMixApp().run()