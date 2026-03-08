[app]
title = VOL
package.name = voladjuster
package.domain = org.volapp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = ffmpeg
version = 1.0
requirements = python3,kivy==2.3.0,android
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.archs = arm64-v8a
android.accept_sdk_license = True
android.allow_backup = True
android.release_artifact = apk
orientation = portrait
fullscreen = 0
android.presplash_color = #0a0a0a
android.gradient_color = #0a0a0a

[buildozer]
log_level = 2
warn_on_root = 1
