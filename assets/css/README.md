# CSS - Cấu trúc và thứ tự nạp

Trước đây toàn bộ nằm trong một file `style.css` (~3.970 dòng). Nay đã tách
theo từng trang để dễ đọc, dễ sửa và dễ tìm kiếm.

## Danh sách file (theo thứ tự nạp)

| # | File | Dòng | Nội dung |
|---|------|-----:|----------|
| 1 | `reset.css` | 64 | Chuẩn hoá lại mặc định của trình duyệt |
| 2 | `base.css` | 114 | Biến màu/font/kích thước, `box-sizing`, style gốc cho `body`, tiêu đề |
| 3 | `components.css` | 402 | `.container`, `.section`, `.btn`, `.tag`, khung ảnh, **thẻ sách** + responsive |
| 4 | `layout.css` | 445 | Header, menu, ô tìm kiếm, footer + responsive của chúng |
| 5 | `home.css` | 449 | Hero, thể loại, banner, vì sao chọn, đánh giá, nhận tin (chỉ trang chủ) |
| 6 | `login.css` | 186 | Trang đăng nhập |
| 7 | `book.css` | 435 | Trang chi tiết sách (chứa cả `.breadcrumb` và `.qty` dùng lại) |
| 8 | `cart.css` | 414 | Trang giỏ hàng (chứa cả khối `.cart-summary` dùng lại) |
| 9 | `admin.css` | 513 | Trang quản trị: bố cục, sidebar, thanh trên, thẻ số liệu, biểu đồ |
| 10 | `admin-data.css` | 557 | Trang quản trị: danh sách, bảng dữ liệu, bộ lọc, phân trang |
| 11 | `checkout.css` | 384 | Trang thanh toán |
| 12 | `compat.css` | 69 | Fallback cho trình duyệt cũ - **luôn nạp cuối cùng** |

> Thứ tự trong bảng là thứ tự ưu tiên (cascade). Nếu thêm file mới, hãy chèn
> đúng vị trí để các file sau vẫn được ghi đè lên file trước.

## Trang nạp những file nào

| Trang | Nạp thêm (sau `reset.css`) |
|-------|---------------------------|
| `index.html` | base → components → layout → home → compat |
| `book.html` | base → components → layout → book → compat |
| `cart.html` | base → components → layout → **book** → cart → compat |
| `checkout.html` | base → components → layout → **book** → **cart** → checkout → compat |
| `login.html` | base → components → layout → login → compat |
| `admin.html` | base → components → layout → admin → admin-data → compat |

`cart.html` và `checkout.html` nạp thêm `book.css` / `cart.css` vì chúng dùng
lại `.breadcrumb`, `.qty` (trang sách) và `.cart-summary` (trang giỏ).

## Font chữ - tại sao KHÔNG dùng Georgia

`--font-heading` phải là font **có đủ ký tự tiếng Việt** (ế, ộ,ữ, ạ, ị...).

- `georgia.ttf` (219 KB) **không** chứa các ký tự này. Nếu Georgia ở đầu stack,
  mỗi chữ có dấu sẽ rơi về font khác: cả từ bị trộn hai kiểu chữ giữa chừng, và
  **mỗi trình duyệt chọn font thay thế khác nhau** nên Chrome/Edge trông khác
  Firefox (đây từng là lỗi "font bị lạ trên Chrome").
- `--font-heading: "Times New Roman", Times, serif` - Times New Roman có đủ dấu
  tiếng Việt trên Windows/macOS/Linux, cả 4 kiểu (regular/bold/italic/bold).
- Không dùng `-webkit-font-smoothing: antialiased`: Firefox bỏ qua khai báo đó
  nên Chrome/Safari trên macOS sẽ làm chữ mảnh hơn, lệch giữa các trình duyệt.

Kiểm tra coverage của một font (PowerShell):

```powershell
Add-Type -AssemblyName PresentationCore
$g = New-Object System.Windows.Media.GlyphTypeface([Uri]"C:\Windows\Fonts\times.ttf")
$g.CharacterToGlyphMap.ContainsKey(0x1EBF)   # True nếu có chữ "ế"
```

