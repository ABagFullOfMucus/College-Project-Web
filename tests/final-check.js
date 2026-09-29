// Cong ngat tong hop cho trang static khong JS:
//  1. CSS can bang ngoac
//  2. Khong co id trung lap tren moi trang
//  3. Moi <label for> deu tro den dieu khien ton tai
//  4. Moi dieu khien trong .field deu duoc nhan bao quan (id hoac label ngam)
//  5. Moi href="#x" cung trang deu tro den id co san
//  6. Moi lien ket noi trang den file .html deu ton tai
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('./domcss.js');

const ROOT = path.join(__dirname, '..');
let pass = 0, fail = 0;
const bad = [];
const ok = () => pass++;
const no = m => { fail++; bad.push(m); };

// --- 1. CSS ---
console.log('=== 1. CSS can bang ngoac ===');
const cssFiles = fs.readdirSync(path.join(ROOT, 'assets/css')).filter(f => f.endsWith('.css'));
for (const f of cssFiles) {
  const s = fs.readFileSync(path.join(ROOT, 'assets/css', f), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');                 // bo comment
  let d = 0, min = 0;
  for (const ch of s) { if (ch === '{') d++; else if (ch === '}') { d--; min = Math.min(min, d); } }
  if (d === 0 && min >= 0) ok();
  else no('CSS le ngoac ' + f + ': depth=' + d + ' min=' + min);
}
console.log('  ' + cssFiles.length + ' file CSS');

// --- cac trang ---
const pages = fs.readdirSync(ROOT).filter(f => f.endsWith('.html')).sort();
console.log('\n=== 2-6. Tung trang ===');

function cssExists(h) {
  const m = h.match(/^(\.\/)?([A-Za-z0-9_-]+\.html)(#.*)?$/);
  return !m || fs.existsSync(path.join(ROOT, m[2]));
}

for (const p of pages) {
  const html = fs.readFileSync(path.join(ROOT, p), 'utf8');
  const doc = new JSDOM(html).window.document;

  // 2. id trung lap
  const seen = new Map();
  for (const n of doc.querySelectorAll('[id]')) seen.set(n.id, (seen.get(n.id) || 0) + 1);
  const dup = [...seen].filter(([, c]) => c > 1);
  if (dup.length) dup.forEach(([id, c]) => no(p + ': id trung #' + id + ' (' + c + ')'));
  else ok();

  // 3. label for ton tai
  for (const lb of doc.querySelectorAll('label[for]')) {
    if (doc.getElementById(lb.htmlFor)) ok();
    else no(p + ': label for="' + lb.htmlFor + '" thieu dieu khien');
  }

  // 4. dieu khien trong .field co nhan bao quan
  for (const ctl of doc.querySelectorAll('.field input, .field select, .field textarea')) {
    const lb = ctl.closest('label');
    const viaFor = ctl.id && doc.querySelector('label[for="' + ctl.id + '"]');
    if (lb || viaFor) ok();
    else no(p + ': dieu khien khong co nhan bao quan (name=' + ctl.getAttribute('name') + ')');
  }

  // 5. href="#x" cung trang
  for (const a of doc.querySelectorAll('a[href^="#"]')) {
    const id = a.getAttribute('href').slice(1);
    if (!id) continue;                                   // "#" thuong la nut len dau trang
    if (doc.getElementById(id)) ok();
    else no(p + ': href="#' + id + '" khong co id');
  }

  // 6. lien ket noi trang den file
  for (const a of doc.querySelectorAll('a[href]')) {
    const h = a.getAttribute('href');
    if (/^(https?:|mailto:|tel:|#|\/\/)/.test(h)) continue;
    if (cssExists(h)) ok();
    else no(p + ': lien ket thieu tệp ' + h);
  }
  console.log('  ' + p + ': ' + seen.size + ' id');
}

console.log('\n=== ' + pass + ' OK, ' + fail + ' LOI ===');
for (const b of bad.slice(0, 40)) console.log('  X ' + b);
if (bad.length > 40) console.log('  ... va ' + (bad.length - 40) + ' nua');
process.exit(fail ? 1 : 0);
