import pysd

# خواندن مدل Vensim
model = pysd.read_vensim("coffee.mdl")

# اجرای مدل
result = model.run()

# نمایش چند سطر اول خروجی
print(result.head())

# ذخیره خروجی در فایل CSV
result.to_csv("result.csv")

print("Model executed successfully!")