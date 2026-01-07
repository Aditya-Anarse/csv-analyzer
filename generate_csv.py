import pandas as pd
import random

rows = 1000  # change to 5000 or 10000 if you want bigger

data = {
    "student_id": range(1, rows + 1),
    "age": [random.randint(18, 25) for _ in range(rows)],
    "marks_math": [random.randint(35, 100) for _ in range(rows)],
    "marks_science": [random.randint(35, 100) for _ in range(rows)],
    "marks_english": [random.randint(35, 100) for _ in range(rows)],
    "attendance_percent": [random.randint(50, 100) for _ in range(rows)],
    "city": random.choices(
        ["Delhi", "Mumbai", "Pune", "Chennai", "Bangalore", "Hyderabad"],
        k=rows
    )
}

df = pd.DataFrame(data)
df.to_csv("large_students_data.csv", index=False)

print("large_students_data.csv created successfully ✅")
