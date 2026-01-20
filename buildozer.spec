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
# NOTA: Incluye libffi y versiones estables para evitar errores
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
# DEJAMOS QUE BUILDOZER ELIJA AUTOMATICAMENTE (Para evitar conflictos)
# android.api = 33

# (int) Minimum API your APK will support.
# android.minapi = 21

# (str) Android NDK version to use
# DEJAMOS QUE BUILDOZER ELIJA AUTOMATICAMENTE
# android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (str) Android additional adb arguments
# android.adb_args = -H 127.0.0.1

# (list) Android application meta-data to set (key=value format)
#android.meta_data =

# (list) Android library project to add (will be added in the
# project.properties automatically.)
#android.library_references =

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (list) Android app theme, default is ok for Kivy-based app
#android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) List of Java classes to add to the compilation
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
android.add_src =

# (list) Android AAR archives to add
#android.add_aars =

# (list) Gradle dependencies to add
#android.gradle_dependencies =

# (bool) Enable AndroidX support. Enable when 'android.gradle_dependencies'
# contains an 'androidx' package, or any package from Kotlin source.
# android.enable_androidx = True

# (list) add java compile options
# this can for example be necessary when importing certain java libraries using the 'android.gradle_dependencies' option
# see https://developer.android.com/studio/write/java8-support for further information
# android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

# (list) Gradle repositories to add {can be necessary for some android.gradle_dependencies}
# please enclose in double quotes 
# android.gradle_repositories = "maven { url 'https://jitpack.io' }"

# (list) Packaging options
# see https://google.github.io/android-gradle-dsl/current/com.android.build.gradle.internal.dsl.PackagingOptions.html
# can be necessary to solve conflicts in gradle_dependencies
# android.packaging_options =

# (list) Java classes to exclude from the compilation
#android.skip_update_options =

# (bool) Skip the verification of the build config
# skip_build_config_check = False

# (str) The format used to package the app for release mode (aab or apk or aar).
# android.release_artifact = aab

# (str) The format used to package the app for debug mode (apk or aar).
# android.debug_artifact = apk

#
# Python for android (p4a) specific
#

# (str) python-for-android fork to use, defaults to upstream (kivy)
#p4a.fork = kivy

# (str) python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) python-for-android specific download directory (local cache), defaults to
# ~/.local/share/python-for-android
#p4a.local_recipes =

# (str) python-for-android hook to enable
#p4a.hook =

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
#p4a.port =

# Control the inclusion of python-for-android scripts in the APK
#android.p4a_whitelist =

# (str) Launchon boot
#android.wakelock = True

# (str) python-for-android distribution to use, defaults to a new distribution
#p4a.dist_name = mydist

# (str) python-for-android SDK to use
#p4a.sdk = 20

# (str) python-for-android NDK to use
#p4a.ndk = 9c

# (bool) whether to install the requirements
#p4a.install_requirements = True

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML file for custom backup rules (see official auto backup documentation)
# android.backup_rules =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
# android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only.
android.accept_sdk_license = True

# (str) The entry point of your application in the Python code
# This is usually the filename of your python script.
# entrypoint = main.py

# (list) List of source files to exclude from the source directory
# The default is to exclude all the dot-files/dirs
# source.exclude_dirs = tests, bin, venv

# (list) List of source files to exclude from the source directory
# source.exclude_patterns = license,images/*/*.jpg

# (list) List of filename patterns to exclude from the final package
# source.exclude_exts = spec

# (list) List of config options to pass to the p4a tool
# p4a.config_options = --no-private --window

# (list) List of extra arguments to pass to the p4a tool
# p4a.extra_args = --dist_name=mydist


#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios
# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output storage, absolute or relative to spec file
# bin_dir = ./bin
