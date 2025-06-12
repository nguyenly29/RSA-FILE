![Screenshot 2025-06-12 072844](https://github.com/user-attachments/assets/703ee3b0-c018-447d-adc0-1e2683511807)
Giới thiệu:
Đây là một ứng dụng web cho phép người dùng tải lên tệp tin, ký số tệp đó bằng khóa RSA, và sau đó xác thực chữ ký số
Chức năng:
Tải lên tệp tin: Người dùng có thể tải lên một tệp tin thông qua giao diện web.
Ký số tệp tin: Sau khi tải lên, tệp tin sẽ được ký số bằng khóa riêng RSA, và chữ ký sẽ được trả về cho người dùng cùng với khóa công khai.
Xác thực chữ ký: Người dùng có thể xác thực chữ ký số bằng cách tải lên tệp tin, chữ ký và khóa công khai đã nhận. Chương trình sẽ kiểm tra xem chữ ký có hợp lệ hay không.
Cách hoạt động:
1. Khởi động server
Ứng dụng Flask khởi động và tạo ra một cặp khóa RSA (khóa riêng và khóa công khai) khi server được khởi động.
2. Các route chính
Route /: Trả về tệp index.html từ thư mục frontend, cung cấp giao diện người dùng.
Route /<path:path>: Phục vụ các tệp tĩnh từ thư mục frontend (như CSS, JS).
Route /sign:
Nhận tệp từ yêu cầu POST.
Lưu tệp vào thư mục uploads.
Đọc nội dung tệp và ký số bằng khóa riêng RSA.
Trả về tên tệp, chữ ký (mã hóa base64) và khóa công khai.
Route /verify:
Nhận tệp, chữ ký và khóa công khai từ yêu cầu POST.
Đọc nội dung tệp và giải mã chữ ký từ base64.
Sử dụng khóa công khai để xác thực chữ ký.
Trả về kết quả xác thực (hợp lệ hay không).
3. Bảo mật
Chương trình sử dụng chuẩn PSS (Probabilistic Signature Scheme) để ký và xác thực chữ ký, đảm bảo tính bảo mật cao.
4. Lưu trữ
Các tệp tin được lưu trữ trong thư mục uploads, và ứng dụng sử dụng secure_filename để đảm bảo an toàn khi lưu tệp.
