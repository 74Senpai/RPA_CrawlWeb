# Mục đích
```py Class CrawlAloNhaDat ```
Lớp `CrawlAloNhaDat` là một lớp được khai báo với mục đích cào dữ liệu nhất định trong trang web AloNhaDat.

## Khai báo & sử dụng 
### 1. Khai báo 
Khai báo `CrawlAloNhat()` để sử dụng các chức năng của lớp

### 2. Sử dụng 
- Cơ bản, mặc định: 
```py
        crawl_data = CrawlAloNhaDat()
        crawl_data.start_crawl()
        crawl_data.chose_type_data_to_find(province, property_type, direction, district, price, square, type_post)
        crawl_data.crawl_data()
        crawl_data.save_data_to_excel()
        crawl_data.end_task()
        crawl_data.send_mail_crawl_state()
```
- Tuy biến : 
Các logic tuy biến phải nằm trong phạm vi giữa `start_crawl` đến `end_task` để đảm bảo `Driver` có dữ liệu và có thể hoạt động đúng như mong muốn.
```py 
    crawl_data = CrawlAloNhaDat()
    crawl_data.start_crawl()
    # Custom logic
    # Tips : sử dụng Self.message để lưu log của Crawler sau đó có thể dùng send_mail_crawl_state() để gửi log về email
    crawl_data.end_task()
```

## Các phương thức chính
#### start_crawl
`start_crawl` là phương thức để bắt đầu một tiến trình Crawl, nó khởi tạo trình điều khiển `Driver` và mở trình duyệt web với `URL` định sẵn.
- nó là một phần không thể thiếu khi bắt đầu một tiến trình Crawl.

### chose_type_data_to_find
`chose_type_data_to_find` là một hàm, ở đó người dùng cần khai báo những lựa chọn những trường thông tin nhằm phục vụ tìm kiếm thông tin theo các lựa chọn đưa vào hàm.
- đây là hàm giúp crawl thông tin cần thiết, tránh dư thừa và giảm tại việc xử lý đầu cuối.
- các tham số đầu vào có thể chứa một giá trị được quy đinh hoặc để trống
- Các `parameter` gồm 
    + `province`: đây là biến định nghĩa tỉnh mà chương trình muốn nhằm tới 
    + `property_type`: đây là loại thuộc tính mà người dùng muốn tập trung vào 
    + `direction`: hướng muốn tìm 
    + `district`: vị trí quận, huyện muốn tìm ( *Lưu ý: quận, huyện phải đúng chính tả và phải tồn tại ở địa phương* )
    + `price`: mức giá muốn tìm     
    + `square`: diện tích 
    + `type_post`: thể loại bài đăng
- xem thêm **các giá trị có thể chọn**

### crawl_data
`crawl_data` là lõi của chương trình, nó gọi tới các phương thức khác của lớp `CrawlAloNhaDat` để thực hiện công việc chính của lớp `CrawlAloNhaDat`, nó thông báo trạng thái và thực hiện các.

### save_data_to_excel
`save_data_to_excel` là phương thức quan trong trong việc lưu trữ thông tin đã lấy được, nó sử dụng thư viện Pandas để xử lý dữ liệu và lưu file dưới dạng Excel ở thư mục do người dùng định nghĩa.

### end_task
`end_task` đúng như tên gọi, đây là phương thức để kết thúc tiến trình `Crawl` của lớp, nó đóng trình điều khiển `Driver`, thông báo và kết thúc tiến trình `Crawl`

### send_mail_crawl_state
`send_mail_crawl_state` : thực hiện việc gửi mail theo cấu hình về trạng thái của quá trình `Crawl`. Gọi hàm sau khi kết thúc chương trình hay sau `end_task` để nhận được thông tin chính xác và đầy đủ nhất.

### Các phương thức khác
- `click_selected_tag` : phương thức thực hiện việc nhấn vào thẻ `<select>` được chỉ định.
- `chose_option_by_element_text` : phương thức thực hiện việc chọn vào một `<option>` với một text chỉ định.
- `chose_option_by_element_value` : phương thức thực hiện việc chọn vào một `<option>` với một giá trị chỉ định.
- `get_value_by_key_name` : phương thức thực hiện việc chọn vào một `<option>` với một tên chỉ định.
- `check_element_exist_in_item` : phương thức kiểm tra sự tồn tại của một item trong một item khác nếu có trả về `True` ngược lại trả về `False`.
- `lay_mot_ta_chi_tiet` : phương thức thực hiện việc mở bài viết và lấy thông tin được mô tả một cách đầy đủ nhất với thư viện `Beautiful Soup` nếu thất bại, lấy chi tiết được khai báo ngắn gọn ở bài viết.
- `get_house_infor_posts` : trong mỗi trang sẽ có những thẻ bài viết, phương thức được sử dụng nhằm lấy tất cả danh sách bài viết có trên mỗi trang, dữ liệu trả về là một `list` nếu trang chứa các bài viết được xác định trước hoặc `None` nếu không tìm thấy.
- `get_house_infor` : phương thức được khai báo với mục đích lấy thông tin của mỗi thẻ bài viết và lưu vào mảng dữ liệu - `self.data` của lớp `CrawlAloNhaDat`. `Parameter` cần truyền vào là một item nằm trong danh sách được hàm `get_house_infor_posts` trả về.
- `get_list_house_infor` : phương thức nhận vào một danh sách từ `get_house_infor_posts` và nhiệm vụ của nó là lấy từng item ra và đưa vào hàm `get_house_infor` để thực hiện trích xuất dữ liệu.
- `click_next_page` : hàm nhận vào một tham số `next_page` có kiểu số nguyên chỉ ra trang tiếp theo cần chuyển tới để tiến hành chuyển trang, khi chuyển trang thành công giá trị trả về là `True` ngược lại `False`.
