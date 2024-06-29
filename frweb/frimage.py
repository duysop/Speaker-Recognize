import mysql.connector

# Kết nối tới cơ sở dữ liệu
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="duy100301",
    database="INFor"
)
cursor = conn.cursor()

# Truy vấn dữ liệu hình ảnh
cursor.execute("SELECT name, image FROM users WHERE id = 1")
result = cursor.fetchone()

# Lưu hình ảnh ra file
if result:
    name, image = result
    with open(name + ".jpg", "wb") as file:
        file.write(image)

cursor.close()
conn.close()