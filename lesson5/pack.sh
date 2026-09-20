#!/bin/sh
set -e
cd "$(dirname "$0")"
OUT="HeroDungeon-第5课-学生作业包.zip"
rm -f "$OUT"
zip -r "$OUT" "学生作业包"
echo "created $(pwd)/$OUT"
