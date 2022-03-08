#!/bin/bash

DESTINATION="${1:-/libs}"
mkdir -p "${DESTINATION}"

libs="
/usr/lib/x86_64-linux-gnu/libodbc*
/usr/lib/x86_64-linux-gnu/libbrotlicommon.so*
/usr/lib/x86_64-linux-gnu/libbrotlidec.so*
/usr/lib/x86_64-linux-gnu/libcurl.so*
/usr/lib/x86_64-linux-gnu/libgcrypt.so*
/usr/lib/x86_64-linux-gnu/libgmp.so*
/usr/lib/x86_64-linux-gnu/libgnutls.so*
/usr/lib/x86_64-linux-gnu/libhogweed.so*
/usr/lib/x86_64-linux-gnu/libidn2.so*
/usr/lib/x86_64-linux-gnu/liblber-2.4.so*
/usr/lib/x86_64-linux-gnu/libldap_r-2.4.so*
/usr/lib/x86_64-linux-gnu/libnettle.so*
/usr/lib/x86_64-linux-gnu/libnghttp2.so*
/usr/lib/x86_64-linux-gnu/libp11-kit.so*
/usr/lib/x86_64-linux-gnu/libpsl.so*
/usr/lib/x86_64-linux-gnu/librtmp.so*
/usr/lib/x86_64-linux-gnu/libsasl2.so*
/usr/lib/x86_64-linux-gnu/libssh2.so*
/usr/lib/x86_64-linux-gnu/libtasn1.so*
/usr/lib/x86_64-linux-gnu/libunistring.so*
"

cp --no-dereference $libs "${DESTINATION}"
