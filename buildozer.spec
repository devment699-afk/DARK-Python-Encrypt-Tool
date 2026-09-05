[app]
title = DARK DEVEL ENC
package.name = darkdevelenc
package.domain = com.dark.develenc

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,plyer,cryptography
orientation = portrait
fullscreen = 0
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk_path = /usr/local/lib/android/sdk
android.accept_sdk_license_agreement = True
p4a.bootstrap = sdl2
p4a.port = 5000
p4a.sdk_dir = /usr/local/lib/android/sdk

[buildozer]
log_level = 2
warn_on_root = 0

