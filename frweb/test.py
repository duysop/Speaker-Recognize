import mysql.connector

# Thiết lập kết nối đến MySQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="duy100301",
  database="INFor"
)

# Hàm để lấy thông tin người dùng từ cơ sở dữ liệu
def get_user_info(user_id):
    try:
        # Tạo cursor để thực hiện truy vấn
        cursor = mydb.cursor()

        # Truy vấn để lấy thông tin của người dùng
        query = "SELECT id, name, email, phone FROM users WHERE name = %s"
        cursor.execute(query, (user_id,))

        # Lấy kết quả từ cursor
        user_info = cursor.fetchone()

        # Đóng cursor sau khi sử dụng
        cursor.close()

        return user_info  # Trả về tuple chứa thông tin của người dùng
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Ví dụ sử dụng hàm để lấy thông tin của người dùng với user_id cụ thể
# user_id = 'F1'  # Ví dụ: ID của người dùng được dự đoán
# user_info = get_user_info(user_id)
# if user_info:
#     print(f"Thông tin của người dùng với ID {user_id}:")
#     print(f"ID: {user_info[0]}")
#     print(f"Tên: {user_info[1]}")
#     print(f"Email: {user_info[2]}")
#     print(f"Số điện thoại: {user_info[3]}")
# else:
#     print(f"Không tìm thấy thông tin người dùng với ID {user_id}")
cursor = mydb.cursor()

# Đọc dữ liệu hình ảnh
with open("C:/Users/duyma/Documents/GitHub/Speaker-Recognize/image/14.jfif", "rb") as file:
    binary_data = file.read()

# Chèn dữ liệu hình ảnh vào bảng
sql = "INSERT INTO users (id, name, email, phone, image) VALUES (15, 'F15', 'f15@gmail.com', '461478250', %s)"
# sql = "UPDATE users SET image=%s where name='F2';"
cursor.execute(sql, (binary_data,))


print(cursor.rowcount, "record inserted.")
# for day in range(1, 31):  # Assuming a maximum of 31 days
    
#     cursor.execute(f"""
#         UPDATE monthly_attendance_june_2024 ma
#         JOIN attendance_history ah
#         ON ma.name = ah.name
#         SET ma.day{day} = TRUE
#         WHERE DATE(ah.timestamp) = '{2024}-{str(6).zfill(2)}-{str(day).zfill(2)}'
#     """)
mydb.commit()
cursor.close()
mydb.close()