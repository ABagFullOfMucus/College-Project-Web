// [F] Moi noi dung duoc bat bang :target deu phai co "nut" tro toi:
// either <a href="#id"> or <form action="#id">. Id co the dang nam tren mỏ neo
// (da doi tu id -> class) nen phai lay id qua anchorId, khong lay truc tiep el.id.
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('./domcss.js');

const ROOT = path.join(__dirname, '..');
const REVEALED = '.admin-notice, .confirm, .order-detail-row, .notice';

function anchorId(el, doc) {
  if (el.id) return el.id;
  for (const cl of [...el.classList]) {
    const k = cl.lastIndexOf('--');
    if (k < 0) continue;
    const m = cl.slice(k + 2);
    if (m && doc.getElementById(m)) return m;
  }
  return null;
}

// Nhom noi dung :target chua co nut tro toi, CO SAN TU TRUOC (van con nguyen
// tai HEAD) — khong phai loi cua viec doi sang mỏ neo. Chi la noi dung du
// phong trong kho "thong bao chung" cua index.html; lien he that cua trang
// nam o muc #contact (dang duoc nav tro toi). Giu lai danh sach nay de no
// khong bi lan vao cac loi moi.
const KNOWN_UNUSED = new Set(['index.html#lien-he']);

let pass = 0, fail = 0, skip = 0;
const bad = [];

const PAGES = fs.readdirSync(ROOT).filter(f => f.endsWith('.html')).sort();
for (const p of PAGES) {
  const doc = new JSDOM(fs.readFileSync(path.join(ROOT, p), 'utf8')).window.document;
  const list = [...doc.querySelectorAll(REVEALED)].filter(el => anchorId(el, doc));
  if (!list.length) continue;
  let n = 0;
  for (const el of list) {
    const id = anchorId(el, doc);
    const hasLink = !!doc.querySelector('a[href="#' + id + '"],'
      + 'form[action="#' + id + '"],'
      + 'button[formaction="#' + id + '"]')
      // nut/thep trong trang con tro ve admin.html#id
      || [...doc.querySelectorAll('[href],[action]')].some(e =>
        ((e.getAttribute('href') || '') + (e.getAttribute('action') || '')).includes('#' + id));
    if (hasLink) pass++;
    else if (KNOWN_UNUSED.has(p + '#' + id)) skip++;
    else { fail++; bad.push(p + ': #' + id + ' khong co nut tro toi'); }
    n++;
  }
  console.log('  ' + p + ': ' + n + ' noi dung :target');
}

console.log('\n=== ' + pass + ' OK, ' + fail + ' LOI'
  + (skip ? ' (bo qua ' + skip + ' co san tu truoc: ' + [...KNOWN_UNUSED].join(', ') + ')' : '') + ' ===');
for (const b of bad) console.log('  X ' + b);
process.exit(fail ? 1 : 0);
