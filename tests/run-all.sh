#!/usr/bin/env bash
# Chay toan bo bo kiem tra tinh cua cac trang tinh.
#   cd tests && npm install && npm test        (lan dau)
#   cd tests && bash run-all.sh                (cac lan sau)
#
# LUU Y: jsdom phai la ho 22 — tu 23 tro di no keo theo gói ESM-only
# (@exodus/bytes) khong require() duoc tren Node 18.
set -u
cd "$(dirname "$0")"

ADMIN_PAGES="admin.html admin-book-new.html admin-stock-import.html admin-promo-send.html admin-order-new.html"
fail=0

run() { # $1 = ten hien thi, $2.. = lenh
  local name="$1"; shift
  local out rc last
  out=$("$@" 2>&1); rc=$?
  last=$(printf '%s\n' "$out" | grep -E 'OK, [0-9]+ LOI|BROKEN' | tail -1 | tr -s ' ')
  if [ $rc -eq 0 ]; then
    printf '  \033[32mPASS\033[0m  %-46s %s\n' "$name" "$last"
  else
    printf '  \033[31mFAIL\033[0m  %-46s %s\n' "$name" "$last"
    printf '%s\n' "$out" | tail -12 | sed 's/^/          /'
    fail=1
  fi
}

echo '=== Cong ngat :target (view bi nuot mat => exit 1) ==='
for p in $ADMIN_PAGES; do
  run "target-scan.js $p" node target-scan.js "$p"
done

echo
echo '=== Cac kiem tra hop dong ==='
run 'marker-check.js  (hop dong mỏ neo)'   node marker-check.js
run 'visible-check.js (hien thi .confirm)'  node visible-check.js
run 'link-check.js    (moi noi dung co nut)' node link-check.js
run 'final-check.js   (CSS/id/label/link)'  node final-check.js

echo
if [ $fail -eq 0 ]; then
  echo 'TOT CA BO KIEM TRA DEU DAT.'
else
  echo 'CO KIEM TRA THAT BAI — xem chi tiet o tren.'
fi
exit $fail
