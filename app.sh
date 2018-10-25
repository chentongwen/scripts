#!/bin/bash
set -e
trap clean INT TERM EXIT

KEYS=( "execName" "version")

clean(){
	if [ ! -z ${TEMPDIR} ];then
		rm -rf ${TEMPDIR}
	fi
	rm -f $(json_query desktopName).desktop
}

json_query(){
	result=$(jq -r .$1 app.json 2>/dev/null)
	if [ x"${result}" == x"null" ] || [ x"${result}" == x ];then
		echo "[error] lack of \"$1\", please check app.json" >&2
		exit 1
	fi
	echo ${result}
}


gen_desktop(){
mkdir -p ${TEMPDIR}/usr/share/applications
DESKTOPNAME=$(json_query desktopName).desktop
cat > ${TEMPDIR}/usr/share/applications/${DESKTOPNAME}<<EOF
[Desktop Entry]
Type=Application
Categories=$(json_query categories)
Comment=$(json_query comment)
Comment[zh_CN]=$(json_query chinacomment)
Name=$(json_query displayName)
Name[zh_CN]=$(json_query chinaName)
GenericName[zh_CN]=$(json_query GenericName)
Terminal=false
StartupNotify=false
Icon=$(json_query icon)
Exec=/usr/lib/electron/electron /opt/codemao-webapps/$(json_query execName)
EOF
}


nativefier(){
NATIVEFIER=nativefier.json
cat > ./electron/${NATIVEFIER}<<EOF
{
"name": "$(json_query execName)",
"targetUrl": "$(json_query url)",
"counter": false,
"bounce": false,
"width": 1280,
"height": 833,
"showMenuBar": false,
"fastQuit": false,
"userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36",
"nativefierVersion": "7.6.4",
"ignoreCertificate": false,
"disableGpu": false,
"ignoreGpuBlacklist": false,
"enableEs3Apis": false,
"insecure": false,
"flashPluginDir": "$(json_query flash)",
"diskCacheSize": null,
"fullScreen": false,
"maximize": false,
"zoom": 1,
"internalUrls": null,
"singleInstance": false,
"tray": false,
"basicAuthUsername": null,
"basicAuthPassword": null,
"alwaysOnTop": false
}
EOF
}

packages(){
PACKAGES=package.json
cat > ./electron/${PACKAGES}<<EOF
{
    "name": "$(json_query execName)",
    "version": "$(json_query version)",
    "description": "Placeholder for the nativefier cli to override with a target url",
    "main": "lib/main.js",
    "dependencies": {
        "electron-context-menu": "^0.9.1",
        "electron-dl": "^1.10.0",
        "electron-window-state": "^4.1.1",
        "loglevel": "^1.5.1",
        "source-map-support": "^0.5.0",
        "wurl": "^2.5.2"
    },
    "devDependencies": {},
    "scripts": {
        "test": "echo \"Error: no test specified\" && exit 1"
    },
    "keywords": [
        "desktop",
        "electron"
    ],
    "author": "Jia Hao",
    "license": "MIT"
}
EOF
}

build(){
	TEMPDIR=`mktemp -d -p $(pwd)`
	gen_desktop
	nativefier
	packages
}



package(){
	local NAME=$(json_query execName)
	local DESKTOPNAME=$(json_query desktopName).desktop
	mkdir -p ${TEMPDIR}/DEBIAN
	mkdir -p ${TEMPDIR}/opt/codemao-webapps/${NAME}
	mkdir -p ${TEMPDIR}/usr/share/icons/elementary/apps/64
	cp -r electron/* ${TEMPDIR}/opt/codemao-webapps/${NAME}
	echo ${TEMPDIR}/usr/share/icons/elementary/apps/* | xargs -n 1 cp -i $(json_query icon).svg
	local size=$(/usr/bin/du -sk --apparent-size ${TEMPDIR})
	size="$(( ${size%%[^0-9]*} ))"
	cat > ${TEMPDIR}/DEBIAN/control <<EOF
Package: ${NAME}
Version: $(json_query version)
Section: Net
Priority: extra
Architecture: amd64
Depends: libc6 (>= 2.3.5-1), electron
Installed-Size: ${size}
Maintainer: codemao <package@codemao.cn>
Description: $(json_query comment)
EOF
	touch ${TEMPDIR}/DEBIAN/postinst
	chmod a+x ${TEMPDIR}/DEBIAN/postinst
	cat > ${TEMPDIR}/DEBIAN/postinst <<EOF
#!/bin/bash
gtk-update-icon-cache -f /usr/share/icons/elementary/
EOF

	echo "[info] build debian package"
	fakeroot dpkg -b ${TEMPDIR} ${NAME}.deb
}

main(){
	build
	package
}
main
