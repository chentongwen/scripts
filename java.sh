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

wget $(json_query url)
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
Exec=java -jar /opt/java/$(json_query execName)/$(json_query execName).jar
EOF
}

build(){
	TEMPDIR=`mktemp -d -p $(pwd)`
	gen_desktop
}

package(){
	local NAME=$(json_query execName)
	local DESKTOPNAME=$(json_query desktopName).desktop
	mkdir -p ${TEMPDIR}/DEBIAN
	mkdir -p ${TEMPDIR}/opt/java/${NAME}
	mkdir -p ${TEMPDIR}/usr/share/icons/elementary/apps/64
	cp -r *.jar ${TEMPDIR}/opt/java/${NAME}/${NAME}.jar
	echo ${TEMPDIR}/usr/share/icons/elementary/apps/* | xargs -n 1 cp -i $(json_query icon).svg
	local size=$(/usr/bin/du -sk --apparent-size ${TEMPDIR})
	size="$(( ${size%%[^0-9]*} ))"
	cat > ${TEMPDIR}/DEBIAN/control <<EOF
Package: ${NAME}
Version: $(json_query version)
Section: Net
Priority: extra
Architecture: amd64
Depends: libc6 (>= 2.3.5-1)
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
