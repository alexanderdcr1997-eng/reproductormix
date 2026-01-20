[app]

# (str) Title of your application
title = DALEMIX

# (str) Package name
package.name = dalemix

# (str) Package domain (needed for android/ios packaging)
package.domain = org.dalemix

# (str) Source code where the main.py live
source.dir = .

# (str) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# NOTA: Agregamos libffi y quitamos restricciones raras
requirements = python3,kivy==2.2.1,kivymd,yt-dlp,openssl,requests,urllib3,chardet,idna,libffi

# (str) Custom source folders to include
# source.include_patterns = assets/*,images/*.png

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (list) List of service to declare
# services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,FOREGROUND_SERVICE,WAKE_LOCK,READ_MEDIA_AUDIO

# (int) Target Android API, should be as high as possible.
# DEJAMOS QUE BUILDOZER ELIJA AUTOMATICAMENTE (Comentado con #)
# android.api = 33

# (int) Minimum API your APK will support.
# android.minapi = 21

# (str) Android NDK version to use
# DEJAMOS QUE BUILDOZER ELIJA AUTOMATICAMENTE (Comentado con #)
# android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (str) Android additional adb arguments
# android.adb_args = -H 127.0.0
