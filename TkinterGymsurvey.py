import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt

# Database setup
def setup_database():
    conn = sqlite3.connect('gym_survey.db')
    cursor = conn.cursor()
    # Create tables if not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS survey_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age_group TEXT,
            gym_frequency TEXT,
            fitness_goals TEXT,
            session_length TEXT,
            exercise_focus TEXT,
            workout_plan TEXT,
            motivation INTEGER,
            challenges TEXT,
            benefits TEXT
        )
    """)
    conn.commit()
    conn.close()

# Function to submit the form
def submit_form():
    responses = {
        "name": name_entry.get(),
        "age_group": age_var.get(),
        "gym_frequency": freq_var.get(),
        "fitness_goals": ", ".join([goal for goal, var in goal_vars.items() if var.get()]),
        "session_length": session_var.get(),
        "exercise_focus": ", ".join([exercise for exercise, var in exercise_vars.items() if var.get()]),
        "workout_plan": plan_var.get(),
        "motivation": int(motivation_scale.get()),
        "challenges": ", ".join([challenge for challenge, var in challenge_vars.items() if var.get()]),
        "benefits": ", ".join([benefit for benefit, var in benefit_vars.items() if var.get()])
    }

    # Save data to database
    try:
        conn = sqlite3.connect('gym_survey.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO survey_responses (name, age_group, gym_frequency, fitness_goals, session_length,
                                          exercise_focus, workout_plan, motivation, challenges, benefits)
            VALUES (:name, :age_group, :gym_frequency, :fitness_goals, :session_length,
                    :exercise_focus, :workout_plan, :motivation, :challenges, :benefits)
        """, responses)
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Your responses have been submitted!")
        root.destroy()
        visualize_data()  # Call the visualization function after form submission
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving your responses: {e}")

# Function to visualize data
def visualize_data():
    try:
        conn = sqlite3.connect('gym_survey.db')
        cursor = conn.cursor()
        cursor.execute("SELECT fitness_goals FROM survey_responses")
        rows = cursor.fetchall()
        conn.close()

        # Count fitness goals
        goal_counts = {}
        for row in rows:
            goals = row[0].split(", ")
            for goal in goals:
                if goal in goal_counts:
                    goal_counts[goal] += 1
                else:
                    goal_counts[goal] = 1

        # Prepare data for plotting
        goals = list(goal_counts.keys())
        counts = list(goal_counts.values())

        # Create a bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(goals, counts, color='skyblue')
        plt.xlabel('Fitness Goals')
        plt.ylabel('Number of Responses')
        plt.title('Distribution of Fitness Goals')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while visualizing data: {e}")

# Function to handle user login
def login_user():
    username = username_var.get()
    password = password_var.get()

    try:
        conn = sqlite3.connect('gym_survey.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            open_survey_form()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during login: {e}")
    username_var.set("")
    password_var.set("")

# Function to register a new user
def register_user():
    username = reg_username_var.get()
    password = reg_password_var.get()

    if username and password:
        try:
            conn = sqlite3.connect('gym_survey.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Registration successful!")
            registration_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists. Choose a different username.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while registering: {e}")
    else:
        messagebox.showerror("Error", "Both username and password are required.")

# Function to open the survey form
def open_survey_form():
    login_window.destroy()

    global root, name_entry, age_var, freq_var, goal_vars, session_var, exercise_vars, plan_var, motivation_scale, challenge_vars, benefit_vars

    root = tk.Tk()
    root.title("Gym Habits & Fitness Goals Survey")
    root.geometry("600x700")

    # Create a canvas and scrollbar
    canvas = tk.Canvas(root, borderwidth=0)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    # Configure the canvas to scroll
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Place canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Header
    header = tk.Label(scrollable_frame, text="Gym Habits & Fitness Goals Survey", font=("Arial", 16, "bold"))
    header.pack(pady=10)

    frame = ttk.Frame(scrollable_frame, padding="10")
    frame.pack(fill="both", expand=True)

    # Name field
    name_label = ttk.Label(frame, text="Name:")
    name_label.grid(row=0, column=0, sticky="w", pady=5)
    name_entry = ttk.Entry(frame, width=40)
    name_entry.grid(row=0, column=1, pady=5)

    # Age group
    age_label = ttk.Label(frame, text="What is your age group?")
    age_label.grid(row=1, column=0, sticky="w", pady=5)
    age_var = tk.StringVar(value="Under 18")
    age_choices = ["Under 18", "18–24", "25–34", "35–44", "45–54", "55 and above"]
    age_menu = ttk.OptionMenu(frame, age_var, *age_choices)
    age_menu.grid(row=1, column=1, pady=5)

    # Gym frequency
    freq_label = ttk.Label(frame, text="How often do you go to the gym?")
    freq_label.grid(row=2, column=0, sticky="w", pady=5)
    freq_var = tk.StringVar(value="Daily")
    freq_choices = ["Daily", "3–5 times a week", "1–2 times a week", "Less than once a week", "Never"]
    freq_menu = ttk.OptionMenu(frame, freq_var, *freq_choices)
    freq_menu.grid(row=2, column=1, pady=5)

    # Fitness goals
    goal_label = ttk.Label(frame, text="What are your primary fitness goals? (Select all that apply)")
    goal_label.grid(row=3, column=0, sticky="w", pady=5)
    goal_vars = {goal: tk.BooleanVar() for goal in ["Building muscle", "Losing weight", "Improving endurance", "Increasing flexibility", "Reducing stress"]}
    for i, (goal, var) in enumerate(goal_vars.items()):
        cb = ttk.Checkbutton(frame, text=goal, variable=var)
        cb.grid(row=4 + i, column=0, sticky="w", padx=20)

    # Session length
    session_label = ttk.Label(frame, text="How long do you typically spend at the gym per session?")
    session_label.grid(row=9, column=0, sticky="w", pady=5)
    session_var = tk.StringVar(value="30–60 minutes")
    session_choices = ["Less than 30 minutes", "30–60 minutes", "1–2 hours", "More than 2 hours"]
    session_menu = ttk.OptionMenu(frame, session_var, *session_choices)
    session_menu.grid(row=9, column=1, pady=5)

    # Exercise focus
    exercise_label = ttk.Label(frame, text="Which types of exercises do you focus on at the gym? (Select all that apply)")
    exercise_label.grid(row=10, column=0, sticky="w", pady=5)
    exercise_vars = {exercise: tk.BooleanVar() for exercise in ["Strength training", "Cardio", "Flexibility", "Functional training", "High-intensity interval training"]}
    for i, (exercise, var) in enumerate(exercise_vars.items()):
        cb = ttk.Checkbutton(frame, text=exercise, variable=var)
        cb.grid(row=11 + i, column=0, sticky="w", padx=20)

    # Workout plan
    plan_label = ttk.Label(frame, text="Do you follow a specific workout plan or routine?")
    plan_label.grid(row=16, column=0, sticky="w", pady=5)
    plan_var = tk.StringVar(value="Yes, I have a structured plan")
    plan_choices = ["Yes, I have a structured plan", "Somewhat, I follow a loose routine", "No, I go with what I feel like doing"]
    plan_menu = ttk.OptionMenu(frame, plan_var, *plan_choices)
    plan_menu.grid(row=16, column=1, pady=5)

    # Motivation scale
    motivation_label = ttk.Label(frame, text="On a scale of 1 to 5, how motivated do you feel to achieve your fitness goals?")
    motivation_label.grid(row=17, column=0, sticky="w", pady=5)
    motivation_scale = ttk.Scale(frame, from_=1, to=5, orient="horizontal")
    motivation_scale.grid(row=17, column=1, pady=5)

    # Challenges
    challenge_label = ttk.Label(frame, text="What challenges do you face in maintaining a regular gym routine? (Select all that apply)")
    challenge_label.grid(row=18, column=0, sticky="w", pady=5)
    challenge_vars = {challenge: tk.BooleanVar() for challenge in ["Lack of time", "Lack of motivation", "Financial cost of gym membership", "Not knowing which exercises to do"]}
    for i, (challenge, var) in enumerate(challenge_vars.items()):
        cb = ttk.Checkbutton(frame, text=challenge, variable=var)
        cb.grid(row=19 + i, column=0, sticky="w", padx=20)

    # Benefits
    benefit_label = ttk.Label(frame, text="Have you noticed any benefits from going to the gym? (Select all that apply)")
    benefit_label.grid(row=23, column=0, sticky="w", pady=5)
    benefit_vars = {benefit: tk.BooleanVar() for benefit in ["Increased strength or endurance", "Improved mood or reduced stress", "Better sleep", "Weight management", "Improved energy levels"]}
    for i, (benefit, var) in enumerate(benefit_vars.items()):
        cb = ttk.Checkbutton(frame, text=benefit, variable=var)
        cb.grid(row=24 + i, column=0, sticky="w", padx=20)

    # Submit button
    submit_button = ttk.Button(frame, text="Submit", command=submit_form)
    submit_button.grid(row=30, column=0, columnspan=2, pady=20)

    root.mainloop()

# Login Window
login_window = tk.Tk()
login_window.title("User Login")
login_window.geometry("300x200")

username_var = tk.StringVar()
password_var = tk.StringVar()

tk.Label(login_window, text="Username:").pack(pady=5)
tk.Entry(login_window, textvariable=username_var).pack(pady=5)

tk.Label(login_window, text="Password:").pack(pady=5)
tk.Entry(login_window, textvariable=password_var, show="*").pack(pady=5)

login_button = ttk.Button(login_window, text="Login", command=login_user)
login_button.pack(pady=10)

# Registration Button
def open_registration_window():
    global registration_window, reg_username_var, reg_password_var
    registration_window = tk.Toplevel(login_window)
    registration_window.title("Register")
    registration_window.geometry("300x200")

    reg_username_var = tk.StringVar()
    reg_password_var = tk.StringVar()

    tk.Label(registration_window, text="Username:").pack(pady=5)
    tk.Entry(registration_window, textvariable=reg_username_var).pack(pady=5)

    tk.Label(registration_window, text="Password:").pack(pady=5)
    tk.Entry(registration_window, textvariable=reg_password_var, show="*").pack(pady=5)

    register_button = ttk.Button(registration_window, text="Register", command=register_user)
    register_button.pack(pady=10)

# Button to open the registration window
register_button = ttk.Button(login_window, text="Register", command=open_registration_window)
register_button.pack(pady=5)

# Start the database setup
setup_database()

# Run the login window
login_window.mainloop()
