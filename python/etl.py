#   تمیزکاری:

#  import pandas as pd

#   خواندن فایل CSV
#  df = pd.read_csv("customers.csv")

#  print("قبل از تمیزکاری:")
#  print(df)


#   تمیزکاری:
#   حذف رکوردهای ناقص
#  df = df.dropna()

#   پاکسازی رشته‌ها
#  df['name'] = df['name'].astype(str).str.strip()

#  print("\nبعد از تمیزکاری:")
#  print(df)



#   اتصال به دیتابیس:
#  import psycopg2

#  اتصال:
#  conn = psycopg2.connect(
#      host="localhost",
#      database="postgres",
#      user="postgres",
#      password="sa4xact"
#  )

#  print("connection is done!")


#   ساخت جدول در PostgreSQL با Python:
#  آماده اجرای SQL:
#  cursor = conn.cursor()


#   ساخت جدول
#  اجرای دستور: execute()
#  cursor.execute("""
#  CREATE TABLE IF NOT EXISTS customers (
#           id INT PRIMARY KEY,
#           name TEXT,
#           city TEXT
#  )               
#  """)

#  print("Table is builded")

#  cursor.execute("DELETE FROM customers")


#   Load دیتا:
#  for index, row in df.iterrows():
#      cursor.execute("""
#          INSERT INTO customers (id, name, city)
#          VALUES (%s, %s, %s)
#      """, (row['id'], row['name'], row['city']))

#  commit:ذخیره
#  conn.commit()

#   بستن
#  cursor.close()
#  conn.close()


#  #********* Raveshe herfei baraye code bala: *********#

#   """ import pandas as pd
#   import psycopg2


#    ✅ 1. Extract + Transform
#   def extract_transform(file_path):
#       print("🔹 خواندن CSV...")
#       df = pd.read_csv(file_path)

#       print("🔹 تمیزکاری داده...")
#       df = df.dropna()
#       df['name'] = df['name'].astype(str).str.strip()

#       return df


#    ✅ 2. اتصال به دیتابیس
#   def get_connection():
#       conn = psycopg2.connect(
#           host="localhost",
#           database="postgres",
#           user="postgres",
#           password="PASSWORD_TU"
#       )
#       return conn


#    ✅ 3. ساخت جدول
#   def create_table(cursor):
#       cursor.execute("DROP TABLE IF EXISTS customers")

#       cursor.execute("""
#       CREATE TABLE customers (
#           id INT PRIMARY KEY,
#           name TEXT,
#           city TEXT
#       )
#       """)


#    ✅ 4. Load دیتا
#   def load_data(df, cursor):
#       print("🔹 وارد کردن داده‌ها...")

#       for index, row in df.iterrows():
#           cursor.execute("""
#               INSERT INTO customers (id, name, city)
#               VALUES (%s, %s, %s)
#           """, (row['id'], row['name'], row['city']))


#    ✅ 5. اجرای کل ETL
#   def run_etl():
#       df = extract_transform("customers.csv")

#       conn = get_connection()
#       cursor = conn.cursor()

#       create_table(cursor)
#       load_data(df, cursor)

#       conn.commit()

#       cursor.close()
#       conn.close()

#       print("✅ ETL کامل انجام شد")


#    ✅ اجرای برنامه
#   if __name__ == "__main__":
#       run_etl()



##********* khandane file khame orders.csv: *********##

# orders.csv
#    ↓
# (Extract) → خواندن فایل
#    ↓
# (Transform) →
#    ✅ dropna()
#    ✅ strip()
#    ✅ title()
#    ✅ drop_duplicates(subset=...)
#    ↓
# Load (مرحله بعدی)

import pandas as pd
df = pd.read_csv("orders.csv")

print("قبل:")
print(df)


# ✅ حذف NUL
df = df.dropna()
print("\nبعد از حذف NULL:")
print(df)


# ✅ حذف فاصله
df['customer_name'] = df['customer_name'].str.strip()
df['city'] = df['city'].str.strip()

print('Hazfe Fasele!') 
print(df)

for name in df['customer_name']:
    print(f"'{name}'")
    

    # ✅ یکسان‌سازی حروف
    df['customer_name'] = df['customer_name'].str.title()
    df['city'] = df['city'].str.title()
    print('Yeksansazi!')
    print(df)


    #✅ حذف Duplicate (داده‌های تکراری): 
    # (drop_duplicates()کل سطر را چک می‌کند)

    df = df.drop_duplicates()
   
    print("بعد از حذف duplicate ✅") 
    print(df)

    # فقط این ستون‌ها مهمن: customer_name + city + amount 
    # (subset=[…]فقط ستون‌های مهم را چک می‌کند ✅)

    df = df.drop_duplicates(subset=['customer_name', 'city', 'amount'])

    print(" بعد از حذف duplicate ba subset ✅") 
    print(df)




 #df = pd.read_csv("orders.csv")
 #print(df)



#🟢 Step 1: اتصال به PostgreSQL 

import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="sa4xact"
)

cursor = conn.cursor()

#🟢 Step 2: ساخت جدول clean_orders

cursor.execute(""" 
DROP TABLE IF EXISTS clean_orders;
CREATE TABLE clean_orders (
               order_id INT,
               customer_name TEXT,
               city TEXT,
               amount INT
)
""")

#🟢 Step 3: Load داده‌ها
for index, row in df.iterrows():
    cursor.execute(""" 
        INSERT INTO clean_orders (order_id, customer_name, city, amount)
        VALUES (%s,%s,%s,%s)
""", (row['order_id'], row['customer_name'], row['city'], row['amount']))
    
#🟢 Step 4: ذخیره و بستن
conn.commit()

cursor.close()
conn.close()

print("Data loaded to postgreSQL")