#!/bin/bash
for x in `ls 第三期`
do
sudo cp deb/3/${x}*.deb  第三期/${x}
sudo cp dist/${x}/package.json  第三期/${x}
done
