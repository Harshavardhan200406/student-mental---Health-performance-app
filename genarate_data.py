import pandas as pd
import numpy as np

# Set seed for reproducibility
np.random.seed(42)

# 1. Generate Data (3000 students)
n_samples = 3000 

study_hours = np.random.randint(1, 10, n_samples)
attendance = np.random.randint(50, 100, n_samples)
marks = np.random.randint(40, 100, n_samples)
backlogs = np.random.randint(0, 4, n_samples) # 0 to 3 backlogs
sleep_hours = np.random.randint(4, 10, n_samples)
screen_time = np.random.randint(1, 10, n_samples)

df = pd.DataFrame({
    'StudyHours': study_hours,
    'Attendance': attendance,
    'Marks': marks,
    'Backlogs': backlogs,
    'SleepHours': sleep_hours,
    'ScreenTime': screen_time
})

# 2. DEFINE STRICT LOGIC WITH LIFESTYLE HABITS
def categorize_performance(row):
    b = row['Backlogs']
    m = row['Marks']
    sleep = row['SleepHours']
    screen = row['ScreenTime']
    
    # --- STEP 1: Base Categorization (Backlogs & Marks) ---
    if b == 3 and m < 50:
        category = 'Poor'
    elif b >= 1:
        category = 'Average'
    else: 
        if m >= 75:
            category = 'Excellent'
        elif 65 <= m < 75:
            category = 'Good'
        elif 50 <= m < 65:
            category = 'Average'
        else:
            category = 'Poor'
            
    # --- STEP 2: Lifestyle Habit Modifiers ---
    
    # Penalty 1: Burnout (High marks, but dangerous habits)
    # If they are Good/Excellent, but sleep less than 6 hours AND have 8+ hours screen time
    if category in ['Excellent', 'Good']:
        if sleep < 6 and screen >= 8:
            category = 'Average'
            
    # Penalty 2: Extreme Distraction
    # If they are already Average, but spend 9+ hours on screens, drop to Poor
    elif category == 'Average':
        if screen >= 9:
            category = 'Poor'
            
    # Optional Bonus: The Hard Worker (You can uncomment this if you want to use it)
    # elif category == 'Average' and sleep >= 7 and screen <= 3 and row['StudyHours'] >= 8:
    #     category = 'Good'

    return category

# Apply the function to create the new column
df['Performance'] = df.apply(categorize_performance, axis=1)

# Save to CSV
df.to_csv('student_data.csv', index=False)
print("Success! Generated data with backlogs, marks, sleep, and screen time rules.")