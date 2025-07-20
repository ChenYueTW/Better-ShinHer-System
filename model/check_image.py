import os

allowed_extensions = [".png", ".jpg", ".jpeg"]
invalid_files = []

for filename in os.listdir("data/train"):
    name, ext = os.path.splitext(filename)

    if ext.lower() in allowed_extensions:
        label_part = name.split('_')[0]
        if not (len(label_part) == 4 and label_part.isdigit()):
            invalid_files.append(filename)

if invalid_files:
    print("Error for files in: ")
    for f in invalid_files:
        print(f" - {f}")
else:
    print("ALL CORRECT")