#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinh các trang tĩnh cho Nhà Sách Skibidus.

Site KHÔNG dùng JavaScript và KHÔNG có backend, nên mọi trang đều là HTML tĩnh
được sinh sẵn. Script này chỉ chạy lúc phát triển, KHÔNG chạy trên trình duyệt.

Cấu trúc thư mục: `index.html` là trang duy nhất ở thư mục gốc, các trang còn lại
nằm trong thư mục theo nhóm chức năng:

  categories/the-loai.html                 - trang tổng quan các thể loại
  categories/the-loai-<slug>-trang-<n>.html - danh sách sách theo thể loại, phân trang
  books/book-<slug>.html                   - trang chi tiết từng cuốn sách
  shop/, search/, account/, admin/         - các trang viết tay (không sinh ra)

Trang nằm trong thư mục con nên link tới file ở gốc (index.html, assets/) phải
bắt đầu bằng `../`, riêng khối nhúng vào index.html dùng `./`.

Cách dùng:
  python3 tools/build.py
Sửa khối DATA bên dưới rồi chạy lại lệnh trên.
"""

import html
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Số sách hiển thị trên mỗi trang của trang thể loại
PER_PAGE = 3

# Kích thước thật của từng ảnh bìa, dùng cho thuộc tính width/height để trình
# duyệt dựng sẵn khung, không nhảy bố cục khi ảnh tải xong.
COVERS = {
    "book1.jpg": (1352, 2004),
    "book2.jpg": (2800, 2800),
    "book3.jpg": (663, 984),
    "book4.jpg": (304, 472),
    "book5.jpg": (300, 414),
    "book6.jpeg": (600, 600),
    "book7.jpg": (781, 1231),
    "book8.jpg": (300, 508),
}

# slug | tên hiển thị | icon | mô tả ngắn
CATEGORIES = [
    ("van-hoc", "Văn học", "\U0001F4D6",
     "Tiểu thuyết, truyện ngắn và văn học kinh điển trong nước và thế giới."),
    ("kinh-te", "Kinh tế", "\U0001F4BC",
     "Sách quản trị, đầu tư và tài chính cá nhân cho người đi làm."),
    ("ky-nang-song", "Kỹ năng sống", "\U0001F331",
     "Phát triển bản thân, giao tiếp và xây dựng thói quen bền vững."),
    ("thieu-nhi", "Thiếu nhi", "\U0001F9F8",
     "Truyện thiếu nhi vui nhộn, kèm gợi ý đọc cho người lớn."),
    ("ngoai-ngu", "Ngoại ngữ", "\U0001F30D",
     "Ngữ pháp, từ vựng và đề luyện cho các kỳ thi phổ thông."),
    ("cong-nghe", "Công nghệ", "\U0001F4BB",
     "Lập trình, cơ sở dữ liệu và an toàn thông tin."),
]

# ---------------------------------------------------------------------------
# DANH MỤC SÁCH
# ---------------------------------------------------------------------------
# Mỗi dòng là một cuốn sách, các trường ngăn bằng dấu "|" theo thứ tự:
#
#   slug | tên sách | tác giả | slug thể loại | giá | giá cũ | điểm | số đánh
#   giá | ảnh bìa | nhà xuất bản | năm | số trang | ISBN | 3 điểm nổi bật
#   (ngăn bằng dấu ~) | mô tả
#
# Ngôn ngữ mặc định là tiếng Việt nên không cần khai trong dữ liệu.
DATA = """
mat-biec|Mắt Biếc|Nguyễn Nhật Ánh|van-hoc|89000|110000|4.9|4680|book7.jpg|NXB Văn Học|2020|288|978-604-58-1405-9|Ngôi trường và tuổi thơ trong sắc nét~Câu chuyện về nỗi buồn mà ai cũng từng trải qua~Bài học về tình bạn và sự trưởng thành|Từ một đôi mắt biếc mở ra cả thế giới trẻ thơ của phố Đường Lâm những năm 1960. Bạn học trò gặp gỡ vui vẻ, rồi chạm tới những mất mát đầu tiên của tuổi lớn. Nguyễn Nhật Ánh viết bằng giọng kể trong trẻo, để người đọc thấy lại chính những năm thơ ấu của mình trong ký ức thiếu nhi.
cho-toi-xin-mot-ve-di-tuoi-tho|Cho Tôi Xin Một Vé Đi Tuổi Thơ|Nguyễn Nhật Ánh|van-hoc|78000|104000|4.8|5210|book8.jpg|NXB Văn Học|2021|240|978-604-58-1561-1|Bìa mềm có lời dẫn dành cho người lớn~Một chuyến đi về với ký ức đầy hoài niệm~Về cách sống trọn vẹn giữa guồng quay công việc|Tái bản đặc biệt dành cho người đã đi xa khỏi tuổi thơ, có lời dẫn mới của tác giả. Câu chuyện đi từ một cậu bé nghịch ngợm trên đường phố tới chuyến đi bằng chiếc vé xe buýt xuyên qua nhiều vùng đất, để tìm lại điều đã mất. Sách nói về tình bạn, về lời hứa và về việc không nên đánh mất sự nhạy cảm với cuộc đời.
cay-cam-ngot-cua-toi|Cây Cam Ngọt Của Tôi|José Mauro de Vasconcelos|van-hoc|89000|118000|4.7|4210|book3.jpg|NXB Văn Học|2019|232|978-604-58-1310-8|Hồi ký xúc động và đầy chất thơ~Cậu bé chín nghĩa trong vườn nhà ông nội~Tình yêu thầm lặng của một người cha|Cậu bé chín nghĩa mồ côi được ông nội nhận về nuôi, lớn lên giữa vườn cam và những người thương yêu. Cuốn hồi ký của José Mauro de Vasconcelos được dịch ra hơn hai chục ngôn ngữ, kể một câu chuyện giản dị mà thấm đượm về ơn nghĩa âm thầm của cha cháu.
tuoi-tre-dang-gia-bao-nhieu|Tuổi Trẻ Đáng Giá Bao Nhiêu?|Rosie Nguyễn|van-hoc|75000|95000|4.8|3150|book2.jpg|NXB Lao Động|2022|264|978-604-58-1621-4|Tuyển tập bài viết dành cho người trẻ~Về thời gian, thói quen và sự bình tĩnh~Ngôn ngữ thẳng thắn, dễ đọc và dễ áp dụng|Tuyển tập những bài viết về kỹ năng sống dành cho người trẻ, viết bằng giọng kể gần gũi thay vì khẩu hiệu. Sách đi qua quản lý thời gian, cách xây dựng thói quen, cách giữ bình tĩnh trong cuộc sống nhiều áp lực, kèm bài tập ở cuối mỗi chương để người đọc thử ngay.
de-men-phieu-luu-ky|Dế Mèn Phiêu Lưu Ký|Khue Văn|van-hoc|68000|85000|4.6|2140|book2.jpg|NXB Văn Học|2020|198|978-604-58-1377-2|Phiêu lưu hài hước dành cho thiếu nhi~Nhân vật đầy tính cách và tinh thần hài hước~Sách vừa đọc vừa học được nghề nghiệp báo chí|Câu chuyện phiêu lưu của con dế mèn mơ ước trở thành nhà báo. Từ một con vật nhỏ bé trong vườn, dế mèn lên đường, gặp muôn vàn sự đời và dần hiểu ra sự khắc nghiệt của nghề làm báo. Truyện vui nhưng để lại nhiều bài học về lòng tự trọng và tình bạn.
toi-thay-hoa-vang-tren-co-xanh|Tôi Thấy Hoa Vàng Trên Cỏ Xanh|Nguyễn Nhật Ánh|van-hoc|82000|102000|4.9|3890|book7.jpg|NXB Văn Học|2021|304|978-604-58-1598-7|Chuyện thơ mộng mơ giữa thế giới trẻ thơ~Tình bạn và sức mạnh của lòng trung thực~Nhân vật nhỏ bé nhưng mạnh mẽ trong lời nói|Một cô bé lạc lối tìm về vườn xanh, nơi có những đứa trẻ lớn lên bằng trí tưởng tượng và lời nói trong sự thành thật. Nguyễn Nhật Ánh viết lên thế giới tuổi thơ mà người lớn đọc cũng thấm tay bởi sự trong trẻo và lòng nhân từ trong từng chi tiết nhỏ.
dac-nhan-tam|Đắc Nhân Tâm|Dale Carnegie|ky-nang-song|89000|120000|4.9|2845|book1.jpg|NXB Tổng hợp TP. Hồ Chí Minh|2023|320|978-604-58-1405-9|Nguyên tắc ứng xử giúp bạn được yêu mến ở mọi nơi~Cách góp ý mà không làm tổn thương đối phương~Nghệ thuật lắng nghe và thuyết phục|Ra đời từ năm 1936, Đắc Nhân Tâm vẫn được xem là cuốn sách gối đầu giường về nghệ thuật giao tiếp. Tác phẩm đúc kết từ hàng nghìn buổi thuyết trình và những câu chuyện có thật về những người thành công trong việc xây dựng quan hệ. Sách không dạy mẹo đối nhân xử thế mà hướng tới một nguyên tắc bền vững: hãy thật lòng quan tâm tới người khác.
muon-kiep-nhan-sinh|Muôn Kiếp Nhân Sinh|Nguyễn Phong|ky-nang-song|134400|168000|4.8|2910|book5.jpg|NXB Lao Động|2022|352|978-604-58-1499-1|Nhìn vũ trụ và thời gian bằng con mắt khác~Bài học về sống hạnh phúc ngay trong hiện tại~Ngôn ngữ nhẹ nhàng, đọc như một bài thiền|Những suy nghĩ của tác giả về vũ trụ, ý nghĩa sống và cách sống hạnh phúc, món quà tinh thần cho người đang tìm lại sự bình yên giữa cuộc sống. Sách không giảng phạt mà kể chuyện, để người đọc tự tìm được câu trả lời cho câu hỏi mình đang mang.
atomic-habits|Atomic Habits: Thay Đổi Tí Hon, Hiệu Quả Bất Ngờ|James Clear|ky-nang-song|151200|189000|4.7|5120|book6.jpeg|NXB Thế Giới|2023|296|978-604-58-1621-4|Thói quen nhỏ thay đổi lớn~Cách bỏ dở một thói quen mà không ép bản thân~Bài tập thực hành kèm theo từng chương|Hướng dẫn xây dựng thói quen nhỏ để cải thiện hiệu suất cá nhân: tập trung, lên lịch, bố trí môi trường và phản hồi. Quan niệm trung tâm của sách là thay đổi lớn đến từ thay đổi nhỏ, lặp lại mỗi ngày cho tới khi nó trở thành bản năng.
nghi-giau-lam-giau|Nghĩ Giàu & Làm Giàu|Napoleon Hill|ky-nang-song|96000|120000|4.6|1980|book1.jpg|NXB Tổng hợp TP. Hồ Chí Minh|2021|384|978-604-58-1442-3|Công thức 13 bước rút ra từ nhóm người thành công~Bài học về mục tiêu và lòng quyết tâm~Phong cách truyện kể dễ đọc, không khô khan|Công trình kinh điển được xem là nền tảng của nhiều cuốn sách về phát triển bản thân sau này. Tác giả phân tích thói quen của những người đạt được thành công, rồi rút ra những nguyên tắc áp dụng được cho người đọc ở mọi hoàn cảnh.
song-thong-minh|Sống Thông Minh Lúc Mỗi Tiền Đồng Được Chi|Morgan Housel|ky-nang-song|118000|148000|4.7|1740|book6.jpeg|NXB Lao Động|2023|268|978-604-58-1650-5|Vì sao người giàu và người nghèo hành xử khác nhau~Cách nghĩ về tiền cho người mới bắt đầu~Bài tập lập ngân sách đơn giản, làm được ngay|Mười ba chương ngắn lý giải về cách nhìn của người có tiền khác với người chưa có. Sách không dạy cách trở thành giàu có mà chỉ ra rằng nhiều quyết định tài chính tưởng nhỏ lại quyết định số tiền bạn có khi về già.
ky-nang-lang-nghe|Kỹ Năng Lắng Nghe Và Nói|Đặng Xuân Hải|ky-nang-song|72000|90000|4.5|1560|book5.jpg|NXB Lao Động|2022|212|978-604-58-1503-6|Rèn luyện giao tiếp qua tình huống đời thường~Phân biệt lắng nghe và chờ đợi người khác nói~Bài tập theo cặp kèm hướng dẫn|Sách tập trung vào kỹ năng ít ai dạy đúng: lắng nghe thật sự. Tác giả phân tích những thói quen xấu khiến cuộc trò chuyện hỏng, sau đó đưa ra cách luyện tập cụ thể để người đọc áp dụng được ngay trong công việc lẫn gia đình.
toi-la-gi|Những Đứa Trẻ Chết Bởi|William Golding|thieu-nhi|86000|108000|4.4|1980|book3.jpg|NXB Văn Học|2019|296|978-604-58-1222-3|Tác phẩm đoạt giải Nobel văn học 1983~Bức tranh về bản năng người trong hoàn cảnh khắc nghiệt~Bài học về trách nhiệm và nhóm xã hội|Một đảo hoang chỉ có những đứa trẻ, không người lớn, không luật lệ. Tác giả dựng lên bức tranh về cách bản năng chiếm lĩnh khi tất cả cấu trúc xã hội biến mất, để người đọc tự suy nghĩ về điều làm nên con người.
tuoi-tho-duong-ong|Tuổi Thơ Dữ Dội|Phạm Quỳnh|thieu-nhi|82000|102000|4.6|2640|book8.jpg|NXB Trẻ|2021|212|978-604-58-1612-1|Nhật ký tâm hồn của một nữ sinh lớn lên~Bối cảnh Hà Nội những năm 1980~Những trang viết chân thực về tuổi mười tám|Nhật ký của một nữ sinh lớn lên ở Hà Nội những năm 1980, viết về bài học cuối năm, những mối tình đầu và cả những nỗi buồn không dễ nói thành lời. Bản này giữ nguyên văn phong đặc trưng của tác giả.
de-men-phieu-luu-ky-2|Dế Mèn Phiêu Lưu Ký (Bìa mềm)|Khue Văn|thieu-nhi|72000|90000|4.5|1320|book2.jpg|NXB Văn Học|2020|198|978-604-58-1377-2|Phiêu lưu hài hước, học được nghề báo chí~Nhân vật dế mèn nổi tiếng của tác giả Khue Văn~Tái bản dành cho các bé 8-12 tuổi|Bản in mềm gọn nhẹ phù hợp cho các em nhỏ tự đọc. Câu chuyện phiêu lưu của con dế mèn mơ ước trở thành nhà báo được kể lại nguyên vẹn, kèm gợi ý đọc cho phụ huynh.
lang-anh-1|English Grammar in Use (Bản 5)|Raymond Murphy|ngoai-ngu|168000|210000|4.9|1840|book6.jpeg|Cambridge University Press|2023|396|978-1-318-05858-3|Bài tập tự học ngữ pháp theo từng điểm~Dành cho người trình độ trung cấp~Sách kèm đáp án riêng|Điểm xuất phát chuẩn cho người học tiếng Anh tự học. Mỗi đơn vị giải thích một điểm ngữ pháp rồi cho luyện tập, kèm sách đáp án để tự kiểm tra.
ngu-phap-tieng-anh|Ngữ Pháp Tiếng Anh Cơ Bản|Martin Howard|ngoai-ngu|92000|115000|4.4|980|book4.jpg|NXB Đại học Quốc gia TP. HCM|2021|288|978-604-58-1498-4|Bốn mươi bài ngữ pháp thiết yếu~Bài tập kèm đáp án ở cuối sách~Ghi chú bằng tiếng Việt|Sách dành cho người học lại ngữ pháp từ đầu, trình bày bốn mươi điểm ngữ pháp thiết yếu theo trình tự từ dễ tới khó, mỗi bài có bài tập và phần đáp án riêng.
tu-dien-700-tu|Từ Vựng Tiếng Anh 700 Từ Quan Trọng|Lisa Howarth|ngoai-ngu|128000|160000|4.6|1150|book8.jpg|NXB Đại học Quốc gia TP. HCM|2022|512|978-604-58-1580-1|700 từ phủ 80% văn bản thông thường~Có phiên âm và cách phát âm~Phụ lục từ chuyên ngành|Bảng từ vựng thiết kế cho người Việt, chỉ 700 từ nhưng đủ dùng trong phần lớn văn bản. Mỗi từ có phiên âm, cách phát âm và ví dụ câu.
ky-thuat-phan-mem|Kỹ Thuật Phần Mềm Cơ Bản|Nguyễn Minh Hùng|cong-nghe|142000|178000|4.7|1520|book1.jpg|NXB Khoa học và Kỹ thuật|2022|412|978-604-58-1533-9|Những nguyên tắc không đổi qua mọi ngôn ngữ lập trình~Về yêu cầu, thiết kế và kiểm thử~Có ví dụ thực tế bằng dự án mẫu|Sách nhập môn về phát triển phần mềm, đi từ phân tích yêu cầu, thiết kế, viết mã tới kiểm thử. Tác giả dùng một dự án mẫu xuyên suốt để người đọc thấy các nguyên tắc vận hành ra sao trong thực tế.
co-so-du-lieu|Cơ Sở Dữ Liệu Ứng Dụng|Trần Kim Hải|cong-nghe|126000|157000|4.6|1240|book4.jpg|NXB Khoa học và Kỹ thuật|2021|368|978-604-58-1442-3|Mô hình quan hệ và ngôn ngữ SQL thực hành~Thiết kế lược đồ cơ sở dữ liệu~Kèm sơ đồ ER và câu hỏi ôn|Sách bám sát chương trình môn Cơ sở dữ liệu của các trường đại học, giải thích mô hình quan hệ rồi luyện tập SQL trên các ví dụ có sẵn.
an-minh-khong-mat|An Minh Không Mất|Nguyễn Hoàng Long|cong-nghe|98000|123000|4.5|1080|book5.jpg|NXB Lao Động|2023|304|978-604-58-1640-6|Những thói quen bảo vệ dữ liệu cá nhân~Cách sao lưu và khôi phục đúng cách~Dành cho người không rành công nghệ|Hướng dẫn thực tế để người dùng phổ thông tự bảo vệ dữ liệu của mình: sao lưu định kỳ, đặt mật khẩu mạnh, nhận biết thư giả mạo và xử lý khi tài khoản bị xâm nhập.
kinh-te-hoc-danh-nghiep|Kinh Tế Học Cho Người Mới|Trần Minh Tuấn|kinh-te|104000|130000|4.6|1420|book7.jpg|NXB Lao Động|2022|336|978-604-58-1502-9|Giải thích khái niệm bằng ví dụ đời thường~Cung cầu, cung, giá và thị trường~Phân tích dữ liệu kinh tế căn bản|Giới thiệu kinh tế học cho người mới bắt đầu, từ nguyên tắc cung cầu cung tới cách đọc một bảng số liệu, viết bằng ngôn ngữ đời thường và nhiều ví dụ thực tế.
quet-ban-tam-nhan|Tiết Kiệm Thông Minh|Trương Quốc Bảo|kinh-te|118000|148000|4.7|1710|book2.jpg|NXB Lao Động|2023|248|978-604-58-1612-1|Danh sách thói quen chi tiêu tốt~Bí quyết tích kiệm tiền của người giàu~Có nhiều ví dụ thực tế|Sách tổng hợp các bí quyết tiết kiệm của người đã thành công, từ bỏ thói quen mua theo cảm xúc tới cách tự đặt giới hạn cho mỗi mục chi tiêu.
ky-nang-tai-chinh|Cẩm Nang Quản Lý Tài Chính|Nguyễn Thanh Hà|kinh-te|92000|115000|4.5|1180|book1.jpg|NXB Tổng hợp TP. Hồ Chí Minh|2021|272|978-604-58-1425-1|Lập ngân sách theo quy tắc 50/30/20~Nợ và cách trả nợ không mắc xích lãi~Bảng theo dõi chi tiêu mẫu|Hướng dẫn lập ngân sách, xử lý nợ và đầu tư đầu tiên dành cho người mới bắt đầu quản lý tiền của mình, có bảng theo dõi mẫu để dùng ngay.
toan-lop-12|Giải Toán Lớp 12 Học Kỳ 2|Đỗ Đức Thái|kinh-te|78000|98000|4.4|960|book3.jpg|NXB Giáo dục Việt Nam|2023|284|978-604-58-1651-2|Bài tập theo từng chủ đề trong sách giáo khoa~Lời giải chi tiết từng bài~Kèm phần tự kiểm tra|Sách luyện tập bám sát chương trình Giáo viên, mỗi chủ đề gồm phần tóm tắt kiến thức, bài tập có lời giải và bài tự kiểm tra để luyện thi.
"""
# ---------------------------------------------------------------------------
# PHẦN DỰNG TRANG
# ---------------------------------------------------------------------------

def e(text):
    """Escape ký tự đặc biệt của HTML."""
    return html.escape(str(text), quote=True)


def money(value):
    """89000 -> '89.000đ' (kiểu viết số của Việt Nam)."""
    return "{:,}".format(value).replace(",", ".") + "đ"


def parse_data():
    """Đọc khối DATA thành danh sách sách dạng dict."""
    books = []
    for line in DATA.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        (slug, title, author, cat, price, old, rate, rev, cover,
         pub, year, pages, isbn, highlights, desc) = line.split("|")
        books.append({
            "slug": slug,
            "title": title,
            "author": author,
            "cat": cat,
            "price": int(price),
            "old": int(old),
            "rate": float(rate),
            "rev": int(rev),
            "cover": cover,
            "pub": pub,
            "year": int(year),
            "pages": int(pages),
            "isbn": isbn,
            "highlights": highlights.split("~"),
            "desc": desc,
        })
    return books


CAT_BY_SLUG = {c[0]: c for c in CATEGORIES}


def books_in(cat_slug, books):
    return [b for b in books if b["cat"] == cat_slug]


def discount(book):
    """Phần trăm giảm, làm tròn xuống."""
    return (book["old"] - book["price"]) * 100 // book["old"]


def stars(rate):
    """4.9 -> '★★★★★'. Làm tròn về số sao gần nhất."""
    return "★" * round(rate)


def cover_img(book, css_class, extra="", up="../"):
    w, h = COVERS[book["cover"]]
    return (
        '<img class="{cls}" src="{up}assets/images/books/{cover}" '
        'alt="Bìa sách {title} của tác giả {author}" '
        'width="{w}" height="{h}" {extra}>'
    ).format(
        cls=css_class,
        cover=book["cover"],
        title=e(book["title"]),
        author=e(book["author"]),
        w=w, h=h, extra=extra, up=up,
    )


# --- Các khối dùng chung lấy nguyên văn từ index.html để mọi trang đồng bộ ---

def head(title, desc, page_css, active=""):
    """Khai báo <head>.

    page_css - các file CSS riêng của trang, nạp sau layout.css và trước compat.
    active   - tên mục menu cần tô đậm: "sach-moi" hoặc "the-loai".
    """
    css = "\n\t\t".join('<link rel="stylesheet" href="../assets/css/{0}.css">'.format(c)
                       for c in ["reset", "base", "components", "layout"] + page_css + ["compat"])
    return """<!DOCTYPE html>
<html lang="vi">
	<head>
		<title>{title} - Nhà Sách Skibidus</title>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<meta name="description" content="{desc}">
		<!-- Favicon: dùng chính ảnh logo của thương hiệu -->
		<link rel="icon" type="image/png" href="../assets/images/logo.png">
		<!-- CSS: reset -> base -> components -> layout -> trang -> compat -->
		{css}
	</head>
	<body>
		<a class="skip-link" href="#main">Bỏ qua tới nội dung chính</a>

		<!-- ==================== HEADER ==================== -->
		<header class="site-header">
			<div class="container site-header__inner">
				<a class="logo" href="../index.html">
					<span class="logo__mark" aria-hidden="true">
						<img src="../assets/images/logo.png" alt="" width="96" height="96" decoding="async">
					</span>
					<span class="logo__text">Nhà Sách <strong>Skibidus</strong></span>
				</a>

				<input class="nav-toggle" type="checkbox" id="nav-toggle">
				<label class="nav-toggle__label" for="nav-toggle">
					<span class="visually-hidden">Mở / đóng menu</span>
					<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
				</label>

				<nav class="main-nav" aria-label="Điều hướng chính">
					<ul class="main-nav__list">
						<li><a class="main-nav__link" href="../index.html">Trang chủ</a></li>
						<li><a class="main-nav__link{cls_feat}" href="../index.html#featured">Sách mới</a></li>
						<li><a class="main-nav__link{cls_cat}" href="../categories/the-loai.html">Thể loại</a></li>
						<li><a class="main-nav__link" href="../index.html#promo">Khuyến mãi</a></li>
						<li><a class="main-nav__link" href="../index.html#reviews">Đánh giá</a></li>
						<li><a class="main-nav__link" href="../info/contact.html">Liên hệ</a></li>
					</ul>
				</nav>

				<div class="header-actions">
					<form class="search" role="search" action="../search/search.html" method="get">
						<label class="visually-hidden" for="site-search">Tìm kiếm sách</label>
						<svg class="search__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
						<input class="search__input" id="site-search" name="q" type="search" placeholder="Tên sách, tác giả...">
					</form>

					<a class="cart" href="../shop/cart.html" aria-label="Giỏ hàng, đang có 4 sản phẩm">
						<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M3 4h2l2.4 11h10.2l2-8H6"/><circle cx="9.5" cy="19" r="1.4"/><circle cx="16.5" cy="19" r="1.4"/></svg>
						<span class="cart__count" aria-hidden="true">4</span>
					</a>

					<a class="btn btn--outline btn--sm" href="../account/login.html">Đăng nhập</a>
				</div>
			</div>
		</header>
""".format(title=e(title), desc=e(desc), css=css,
           cls_feat=" main-nav__link--active" if active == "sach-moi" else "",
           cls_cat=" main-nav__link--active" if active == "the-loai" else "")


def footer():
    """Footer lấy nguyên văn từ index.html."""
    return """
		<!-- ==================== FOOTER ==================== -->
		<footer class="site-footer" id="contact">
			<div class="container site-footer__inner">
				<div class="site-footer__col site-footer__col--brand">
					<a class="logo logo--footer" href="../index.html#hero">
						<span class="logo__mark" aria-hidden="true">
							<img src="../assets/images/logo.png" alt="" width="96" height="96" decoding="async">
						</span>
						<span class="logo__text">Nhà Sách <strong>Skibidus</strong></span>
					</a>
					<p class="site-footer__about">Nhà Sách Skibidus — nơi hội tụ tri thức và những trào lưu đọc sách bất tận. Sứ mệnh của chúng tôi là mang đến sách chất lượng, khơi gợi niềm vui khám phá mỗi ngày cho thế hệ trẻ.</p>
					<ul class="social">
						<li>
							<a class="social__link" href="../info/contact.html" aria-label="Facebook">
								<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13.5 21v-7h2.4l.4-2.8h-2.8V9.5c0-.9.3-1.5 1.5-1.5h1.5V5.5c-.3 0-1.3-.1-2.3-.1-2.3 0-3.7 1.3-3.7 3.8v2.1H8v2.8h2.5V21"/></svg>
							</a>
						</li>
						<li>
							<a class="social__link" href="../info/contact.html" aria-label="Instagram">
								<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="16.8" cy="7.2" r="1"/></svg>
							</a>
						</li>
						<li>
							<a class="social__link" href="../info/contact.html" aria-label="YouTube">
								<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="6" width="18" height="12" rx="4"/><path d="m11 9.6 4 2.4-4 2.4Z"/></svg>
							</a>
						</li>
					</ul>
				</div>

				<nav class="site-footer__col" aria-label="Liên kết về chúng tôi">
					<h2 class="site-footer__title">Về chúng tôi</h2>
					<ul class="site-footer__links">
						<li><a href="../categories/the-loai.html">Giới thiệu</a></li>
						<li><a href="../info/contact.html">Tuyển dụng</a></li>
						<li><a href="../index.html#reviews">Tin tức</a></li>
						<li><a href="../info/contact.html">Hợp tác</a></li>
					</ul>
				</nav>

				<nav class="site-footer__col" aria-label="Liên kết hỗ trợ">
					<h2 class="site-footer__title">Hỗ trợ</h2>
					<ul class="site-footer__links">
						<li><a href="../info/contact.html">Chính sách đổi trả</a></li>
						<li><a href="../info/contact.html">Chính sách vận chuyển</a></li>
						<li><a href="../info/contact.html">Câu hỏi thường gặp</a></li>
						<li><a href="../info/contact.html">Bảo mật thông tin</a></li>
					</ul>
				</nav>

				<div class="site-footer__col">
					<h2 class="site-footer__title">Liên hệ</h2>
					<address class="site-footer__contact">
						<span>123 Đường Sách, Phường Bến Thành, TP. Hồ Chí Minh</span>
						<a href="tel:+84901234567">0901 234 567</a>
						<a href="mailto:hotro@nhasachskibidus.vn">hotro@nhasachskibidus.vn</a>
					</address>
					<h3 class="site-footer__title site-footer__title--sm">Phương thức thanh toán</h3>
					<ul class="payments">
						<li class="payments__item">Visa</li>
						<li class="payments__item">Mastercard</li>
						<li class="payments__item">COD</li>
					</ul>
				</div>
			</div>

			<div class="site-footer__bottom">
				<div class="container site-footer__bottom-inner">
					<p class="site-footer__copy">© 2026 Nhà Sách Skibidus. Bảo lưu mọi quyền.</p>
					<ul class="legal">
						<li><a href="../info/contact.html">Điều khoản sử dụng</a></li>
						<li><a href="../info/contact.html">Chính sách bảo mật</a></li>
					</ul>
				</div>
			</div>
		</footer>
	</body>
</html>
"""


def breadcrumb(items):
    """items: danh sách (nhãn, href) — phần tử cuối được coi là trang hiện tại."""
    parts = []
    for i, (label, href) in enumerate(items):
        last = (i == len(items) - 1)
        if last:
            parts.append('<li aria-current="page">{0}</li>'.format(e(label)))
        else:
            parts.append('<li><a href="{0}">{1}</a></li>'.format(href, e(label)))
    return """		<nav class="breadcrumb" aria-label="Đường dẫn">
			<div class="container">
				<ol class="breadcrumb__list">
					{0}
				</ol>
			</div>
		</nav>
""".format("\n\t\t\t\t\t".join(parts))


def back_link(href, label="Quay lại"):
    """Nút quay lại phía trên nội dung trang.

    Site không dùng JavaScript nên không gọi history.back() được: nút luôn trỏ
    về trang cha gần nhất (danh sách thể loại hoặc trang chủ).
    """
    return """\t\t<div class="page-back">
\t\t\t<div class="container">
\t\t\t\t<a class="back-link" href="{0}"><span aria-hidden="true">&larr;</span> {1}</a>
\t\t\t</div>
\t\t</div>
""".format(href, e(label))


def book_card(book, cta="Xem chi tiết", indent=5, up="../"):
    """Một thẻ sách, dùng lại nguyên class .book-card của components.css.

    indent - số tab dùng để thụt lề, để khớp với vị trí khối trong từng file.
    up     - tiền tố đường dẫn về thư mục gốc: "../" với trang trong thư mục con,
             "./" với index.html ở thư mục gốc.
    """
    cat_name = CAT_BY_SLUG[book["cat"]][1]
    t = "\t" * indent
    return """{t}<li class="book-card">
{t}\t<div class="book-card__media">
{t}\t\t<span class="tag tag--sale">-{0}%</span>
{t}\t\t{1}
{t}\t</div>
{t}\t<div class="book-card__body">
{t}\t\t<p class="book-card__category">{2}</p>
{t}\t\t<h3 class="book-card__title"><a href="{up}books/book-{3}.html">{4}</a></h3>
{t}\t\t<p class="book-card__author">{5}</p>
{t}\t\t<p class="book-card__rating">
{t}\t\t\t<span class="stars" aria-hidden="true">{6}</span>
{t}\t\t\t<span class="book-card__rating-value">{7} ({8} đánh giá)</span>
{t}\t\t</p>
{t}\t\t<p class="book-card__price">
{t}\t\t\t<span class="price price--sale">{9}</span>
{t}\t\t\t<span class="price price--old">{10}</span>
{t}\t\t</p>
{t}\t\t<a class="btn btn--primary btn--block" href="{up}books/book-{3}.html">{11}</a>
{t}\t</div>
{t}</li>
""".format(discount(book), cover_img(book, "book-cover", 'loading="lazy" decoding="async"', up=up),
           e(cat_name), book["slug"], e(book["title"]), e(book["author"]),
           stars(book["rate"]), str(book["rate"]).replace(".", ","),
           "{:,}".format(book["rev"]).replace(",", "."),
           money(book["price"]), money(book["old"]), e(cta), t=t, up=up)


def pagination(cat_slug, page, total_pages):
    """Thanh phân trang. Mỗi trang là một file riêng nên bấm là ra trang mới."""
    if total_pages < 2:
        return ""

    def page_url(n):
        if n == 1:
            return "../categories/the-loai-{0}.html".format(cat_slug)
        return "../categories/the-loai-{0}-trang-{1}.html".format(cat_slug, n)

    items = []
    if page > 1:
        items.append('<a class="pagination__link" href="{0}" rel="prev">Trước</a>'.format(page_url(page - 1)))
    else:
        items.append('<span class="pagination__link pagination__link--disabled" aria-hidden="true">Trước</span>')

    for n in range(1, total_pages + 1):
        if n == page:
            items.append('<a class="pagination__link" href="{0}" aria-current="page">{1}</a>'.format(page_url(n), n))
        else:
            items.append('<a class="pagination__link" href="{0}">{1}</a>'.format(page_url(n), n))

    if page < total_pages:
        items.append('<a class="pagination__link" href="{0}" rel="next">Sau</a>'.format(page_url(page + 1)))
    else:
        items.append('<span class="pagination__link pagination__link--disabled" aria-hidden="true">Sau</span>')

    return """			<nav class="pagination" aria-label="Phân trang sách">
				{0}
			</nav>
""".format("\n\t\t\t\t".join(items))


def category_cards(books, indent=5, up="../"):
    """Các thẻ thể loại, dùng chung cho index.html (up="./") và trang thể loại (up="../").

    indent - số tab của thẻ <li>, phải lớn hơn một cấp so với thẻ <ul> chứa nó.
    """
    cards = []
    for slug, name, icon, desc in CATEGORIES:
        n = len(books_in(slug, books))
        cards.append("""{t}<li>
{t}\t<a class="category" href="{up}categories/the-loai-{slug}.html">
{t}\t\t<span class="category__icon" aria-hidden="true">{icon}</span>
{t}\t\t<span class="category__name">{name}</span>
{t}\t\t<span class="category__count">{n} đầu sách</span>
{t}\t</a>
{t}</li>
""".format(slug=slug, icon=icon, name=e(name), n=n, t="\t" * indent, up=up))
    return "".join(cards)


def build_category_index(books):
    """Trang tổng quan: mỗi thể loại một thẻ kèm số sách và trang đầu tiên."""
    cards = category_cards(books)

    return head("Thể loại", "Danh sách Sách theo thể loại: văn học, kinh tế, kỹ năng sống, thiếu nhi, ngoại ngữ và công nghệ.",
                ["book", "category"], active="the-loai") + """
		<main id="main">
""" + breadcrumb([("Trang chủ", "../index.html"), ("Thể loại", None)]) + back_link("../index.html") + """
			<!-- ==================== DANH SÁCH THỂ LOẠI ==================== -->
			<section class="section">
				<div class="container">
					<div class="section__head">
						<p class="eyebrow">Thể loại</p>
						<h1 class="section__title section__title--accent">Khám phá sách theo chủ đề</h1>
						<p class="section__desc">Chọn một thể loại để xem toàn bộ đầu sách của mục đó. Mỗi thể loại được chia thành các trang riêng để bạn dễ xem và dễ tìm.</p>
					</div>

					<ul class="category-grid">
{cards}					</ul>
				</div>
			</section>
		</main>
""".format(cards=cards) + footer()


def build_category_page(cat_slug, page, books):
    """Một trang trong danh sách sách của thể loại."""
    slug, name, icon, desc = CAT_BY_SLUG[cat_slug]
    items = books_in(cat_slug, books)
    total = len(items)
    total_pages = max(1, -(-total // PER_PAGE))          # làm tròn lên
    page = min(page, total_pages)
    chunk = items[(page - 1) * PER_PAGE: page * PER_PAGE]

    cards = "".join(book_card(b, indent=6) for b in chunk)
    crumb_label = name if page == 1 else "{0} - Trang {1}".format(name, page)
    start = (page - 1) * PER_PAGE + 1
    end = min(page * PER_PAGE, total)

    return head(crumb_label, desc, ["book", "category"], active="the-loai") + """
		<main id="main">
""" + breadcrumb([("Trang chủ", "../index.html"), ("Thể loại", "../categories/the-loai.html"), (crumb_label, None)]) + back_link("../categories/the-loai.html", "Quay lại danh sách thể loại") + """
			<!-- ==================== SÁCH THEO THỂ LOẠI ==================== -->
			<section class="section">
				<div class="container">
					<div class="section__head">
						<p class="eyebrow">{icon} Thể loại</p>
						<h1 class="section__title section__title--accent">{name}</h1>
						<p class="section__desc">{desc}</p>
					</div>

					<p class="results__count">Trang {page} / {total_pages} &mdash; hiển thị {start}&ndash;{end} trong tổng số <strong>{total}</strong> đầu sách.</p>

					<ul class="book-grid">
{cards}					</ul>

					{pager}				</div>
			</section>

		</main>
""".format(icon=icon, name=e(name), desc=e(desc), page=page, total_pages=total_pages,
           start=start, end=end, total=total, cards=cards,
           pager=pagination(cat_slug, page, total_pages)) + footer()


def build_book_page(book, books):
    """Trang chi tiết một cuốn sách, dùng lại toàn bộ class của book.css."""
    slug, name, icon, cat_desc = CAT_BY_SLUG[book["cat"]]
    cat_link = "../categories/the-loai-{0}.html".format(slug)
    hl = "".join("\n\t\t\t\t\t\t\t<li>{0}</li>".format(e(h)) for h in book["highlights"])
    saving = book["old"] - book["price"]

    # 4 cuốn cùng thể loại, sắp theo giá tăng dần cho dễ chọn
    same = sorted([b for b in books if b["cat"] == book["cat"] and b["slug"] != book["slug"]],
                  key=lambda b: b["price"])
    related = "".join(book_card(b, indent=6) for b in same[:4])

    return head(book["title"], book["desc"], ["book"], active="sach-moi") + """
		<main id="main">
""" + breadcrumb([("Trang chủ", "../index.html"), ("Thể loại", "../categories/the-loai.html"),
                           (name, cat_link), (book["title"], None)]) + back_link(cat_link, "Quay lại thể loại") + """
			<!-- ==================== CHI TIẾT SÁCH ==================== -->
			<section class="section">
				<div class="container">
					<article class="product">
						<div class="product__gallery">
							<div class="product__frame">
								<span class="tag tag--sale">-{d}%</span>
								{cover}							</div>

							<ul class="product__perks">
								<li class="product__perk">
									<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6l7-3Z"/><path d="m9 11 2 2 4-4"/></svg>
									<span>Sách chính hãng 100%, nhập trực tiếp từ nhà xuất bản.</span>
								</li>
								<li class="product__perk">
									<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 12a8 8 0 1 1-2.7-6"/><path d="M20 4v4h-4"/></svg>
									<span>Đổi trả miễn phí trong 7 ngày nếu sách lỗi in ấn.</span>
								</li>
								<li class="product__perk">
									<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 16V6h10v10"/><path d="M13 9h4l3 3v4h-7"/><circle cx="7" cy="17.5" r="1.6"/><circle cx="17" cy="17.5" r="1.6"/></svg>
									<span>Đóng gói chống sốc, giao toàn quốc từ 1 đến 3 ngày.</span>
								</li>
							</ul>
						</div>

						<div class="product__info">
							<p class="product__category"><a href="{cat_link}">{name}</a></p>
							<h1 class="product__title">{title}</h1>

							<p class="product__meta">Tác giả: <strong>{author}</strong></p>

							<p class="product__rating">
								<span class="stars" aria-hidden="true">{stars}</span>
								<span class="product__rating-value">{rate} ({rev} đánh giá)</span>
							</p>

							<p class="product__price-row">
								<span class="product__price">{price}</span>
								<span class="price price--old">{old}</span>
								<span class="product__save">Tiết kiệm {saving}</span>
							</p>

							<p class="product__stock">
								<span class="product__dot" aria-hidden="true"></span>
								<span>Còn hàng, giao từ 1 đến 3 ngày</span>
							</p>

							<div class="product__buy">
								<div class="qty">
									<label class="qty__label" for="product-qty">Số lượng</label>
									<input class="qty__input" id="product-qty" name="qty" type="number" value="1" min="1" max="99" step="1" inputmode="numeric">
								</div>
								<a class="btn btn--primary" href="#them-vao-gio">Thêm vào giỏ</a>
								<a class="btn btn--outline" href="#mua-ngay">Mua ngay</a>
							</div>

							<p class="product__notice product__notice--target" id="them-vao-gio" tabindex="-1">Đã thêm <strong>{title}</strong> vào giỏ hàng. <a href="../shop/cart.html">Xem giỏ hàng</a></p>

							<p class="product__notice product__notice--target" id="mua-ngay" tabindex="-1">Bạn chọn mua <strong>{title}</strong> với giá {price}. <a href="../shop/cart.html">Tới giỏ hàng</a></p>

							<p class="product__summary">{desc}</p>

							<h2 class="product__subtitle">Điểm nổi bật</h2>
							<ul class="product__highlights">{hl}
							</ul>
						</div>
					</article>
				</div>
			</section>

			<!-- ==================== MÔ TẢ & THÔNG SỐ ==================== -->
			<section class="section section--alt" id="details">
				<div class="container">
					<div class="section__head">
						<p class="eyebrow">Thông tin</p>
						<h2 class="section__title">Mô tả &amp; thông số ấn phẩm</h2>
					</div>

					<div class="detail-grid">
						<div class="detail-block">
							<h3 class="detail-block__title">Giới thiệu nội dung</h3>
							<div class="detail-block__body">
								<p>{desc}</p>
								<p>{cat_desc} Cuốn sách nằm trong chủ đề <a href="{cat_link}">{name}</a> của Nhà Sách Skibidus.</p>
							</div>
						</div>

						<div class="detail-block">
							<h3 class="detail-block__title">Thông số ấn phẩm</h3>
							<dl class="specs">
								<div class="specs__row">
									<dt class="specs__label">Nhà xuất bản</dt>
									<dd class="specs__value">{pub}</dd>
								</div>
								<div class="specs__row">
									<dt class="specs__label">Năm xuất bản</dt>
									<dd class="specs__value">{year}</dd>
								</div>
								<div class="specs__row">
									<dt class="specs__label">Số trang</dt>
									<dd class="specs__value">{pages} trang</dd>
								</div>
								<div class="specs__row">
									<dt class="specs__label">Kích thước</dt>
									<dd class="specs__value">14.5 x 20.5 cm</dd>
								</div>
								<div class="specs__row">
									<dt class="specs__label">Hình thức</dt>
									<dd class="specs__value">Bìa mềm, tay gấp</dd>
								</div>
								<div class="specs__row">
									<dt class="specs__label">Ngôn ngữ</dt>
									<dd class="specs__value">Tiếng Việt</dd>
								</div>
								<div class="specs__row">
									<dt class="specs__label">ISBN</dt>
									<dd class="specs__value">{isbn}</dd>
								</div>
							</dl>
						</div>
					</div>
				</div>
			</section>

			<!-- ==================== SÁCH CÙNG CHỦ ĐỀ ==================== -->
			<section class="section" id="related">
				<div class="container">
					<div class="section__head section__head--row">
						<div>
							<p class="eyebrow">Gợi ý</p>
							<h2 class="section__title section__title--accent">Sách cùng chủ đề {name}</h2>
						</div>
						<a class="btn btn--outline btn--sm" href="{cat_link}">Xem tất cả</a>
					</div>

					<ul class="book-grid">
{related}					</ul>
				</div>
			</section>
		</main>
""".format(d=discount(book), cover=cover_img(book, "product__photo", 'decoding="async"'),
           cat_link=cat_link, name=e(name), title=e(book["title"]), author=e(book["author"]),
           stars=stars(book["rate"]), rate=str(book["rate"]).replace(".", ","),
           rev="{:,}".format(book["rev"]).replace(",", "."),
           price=money(book["price"]), old=money(book["old"]), saving=money(saving),
           desc=e(book["desc"]), hl=hl, cat_desc=e(cat_desc), pub=e(book["pub"]),
           year=book["year"], pages=book["pages"], isbn=e(book["isbn"]),
           related=related) + footer()


FEATURED = ["dac-nhan-tam", "mat-biec", "atomic-habits", "cay-cam-ngot-cua-toi",
            "nghi-giau-lam-giau", "cho-toi-xin-mot-ve-di-tuoi-tho",
            "co-so-du-lieu", "tuoi-tre-dang-gia-bao-nhieu"]


def build_featured_grid(books):
    """Lưới thẻ sách ở trang chủ, sinh từ cùng dữ liệu với các trang thể loại."""
    by_slug = {b["slug"]: b for b in books}
    return "".join(book_card(by_slug[s], indent=6, up="./") for s in FEATURED if s in by_slug)


def replace_region(text, begin, end, body, indent):
    """Thay phần nằm giữa hai comment BEGIN/END bằng `body`.

    `indent` là chuỗi thụt lề dùng cho comment END, để khớp với file đích.
    """
    if begin not in text or end not in text:
        return None
    head, rest = text.split(begin, 1)
    _, tail = rest.split(end, 1)
    return head + begin + "\n" + body + indent + end + tail


def patch_index(books):
    """Điền hai khối sinh tự động trong index.html: lưới thể loại và sách nổi bật.

    index.html là file viết tay, nên chỉ có hai khối được đánh dấu bằng comment
    BEGIN/END mà script này thay thế. Nhờ vậy danh sách ở trang chủ không bao giờ
    lệch với các trang thể loại.
    """
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")

    grid = ('\t\t\t\t<ul class="category-grid">\n' + category_cards(books, indent=5, up="./")
            + '\t\t\t\t</ul>\n')
    text = replace_region(text,
                          "<!-- BEGIN: lưới thể loại, sinh tự động bởi tools/build.py -->",
                          "<!-- END: lưới thể loại -->",
                          grid, "\t\t\t\t")

    cards = ('\t\t\t\t\t<ul class="book-grid">\n' + build_featured_grid(books)
             + '\t\t\t\t\t</ul>\n')
    text = replace_region(text,
                          "<!-- BEGIN: sách nổi bật, sinh tự động bởi tools/build.py -->",
                          "<!-- END: sách nổi bật -->",
                          cards, "\t\t\t\t\t")

    if text is None:
        raise SystemExit("index.html: khong tim thay khoi BEGIN/END "
                         "(can ca 'luoi the loai' va 'sach noi bat')")

    path.write_text(text, encoding="utf-8")
    return "index.html"


def main():
    books = parse_data()

    # Kiểm tra dữ liệu trước khi sinh file, để lỗi lộ ra sớm
    seen = set()
    for b in books:
        assert b["slug"] not in seen, "Trùng slug: " + b["slug"]
        seen.add(b["slug"])
        assert b["cat"] in CAT_BY_SLUG, "Sai thể loại: " + b["cat"]
        assert b["cover"] in COVERS, "Thiếu ảnh bìa: " + b["cover"]
        assert b["old"] > b["price"], "Giá cũ phải lớn hơn giá bán: " + b["slug"]
        assert len(b["highlights"]) == 3, "Cần đúng 3 điểm nổi bật: " + b["slug"]

    for slug in FEATURED:
        assert slug in seen, "FEATURED chứa slug không có trong DATA: " + slug

    written = []

    def write(name, content):
        path = ROOT / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written.append(name)

    write("categories/the-loai.html", build_category_index(books))

    for slug, name, icon, desc in CATEGORIES:
        items = books_in(slug, books)
        total_pages = max(1, -(-len(items) // PER_PAGE))
        for page in range(1, total_pages + 1):
            if page == 1:
                filename = "categories/the-loai-{0}.html".format(slug)
            else:
                filename = "categories/the-loai-{0}-trang-{1}.html".format(slug, page)
            write(filename, build_category_page(slug, page, books))

    for b in books:
        write("books/book-{0}.html".format(b["slug"]), build_book_page(b, books))

    written.append(patch_index(books))

    print("Đã sinh {0} file:".format(len(written)))
    print("  index.html                        - cập nhật khối sách nổi bật")
    print("  categories/the-loai.html          - trang tổng quan thể loại")
    print("  categories/the-loai-*.html        - danh sách theo thể loại, có phân trang")
    print("  books/book-*.html                 - {0} trang chi tiết sách".format(len(books)))


if __name__ == "__main__":
    main()

