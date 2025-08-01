import os
import django
import datetime
import openpyxl
from django.core.files import File

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screen.settings")  # CHANGE THIS
django.setup()

from base.models import Birthday  # CHANGE THIS

# Load Excel
wb = openpyxl.load_workbook("august.xlsx")
sheet = wb.active

PHOTO_DIR = r"C:\Users\Justin George\PycharmProjects\screen\media\photos"  # <--- Set your actual path here

for i, row in enumerate(sheet.iter_rows(min_row=3, values_only=True), start=3):
    srno, code, name, division, mobile, dob_str = row

    if not (code and name and dob_str):
        continue

    if str(dob_str).lower() == "dob":
        print(f"Skipping header row at line {i}")
        continue

    try:
        dob = datetime.datetime.strptime(f"{dob_str} 2024", "%d %b %Y").date()
    except Exception as e:
        print(f"Error parsing DOB for {name}: {dob_str} | Row {i}")
        continue

    photo_path = os.path.join(PHOTO_DIR, f"{code}.jpg")

    birthday = Birthday(
        emp_name=name.strip(),
        emp_code=int(code),
        dob=dob,
    )

    if os.path.exists(photo_path):
        with open(photo_path, 'rb') as img_file:
            birthday.img.save(f"{code}.jpg", File(img_file), save=False)

    birthday.save()


print("Import finished.")
