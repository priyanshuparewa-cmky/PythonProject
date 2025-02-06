# Function to read data from the file and convert to a list of dictionaries
def read_students_from_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            headers = lines[0].strip().split(',') 
            
            students = []
            for line in lines[1:]:
                values = line.strip().split(',')
                student = {headers[i]: (int(values[i]) if i > 0 else values[i]) for i in range(len(headers))}
                students.append(student)
            
            return students
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found. Please ensure the file exists and try again.")
        return []
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return []

# Function to calculate average score for a subject
def average_score(students, subject):
    total = sum(student[subject] for student in students)
    return total / len(students)

def print_average_scores(students):
    for subject in ["math", "science", "history"]:
        print(f"Average {subject.capitalize()} Score: {average_score(students, subject):.2f}")

# Function to find student with the highest score in a subject
def highest_score(students, subject):
    highest = max(students, key=lambda x: x[subject])
    return highest["name"], highest[subject]

def print_highest_scores(students):
    for subject in ["math", "science", "history"]:
        name, score = highest_score(students, subject)
        print(f"Highest {subject.capitalize()} Score: {name} with {score}")

# Function to find student with the lowest score in a subject
def lowest_score(students, subject):
    lowest = min(students, key=lambda x: x[subject])
    return lowest["name"], lowest[subject]

def print_lowest_scores(students):
    for subject in ["math", "science", "history"]:
        name, score = lowest_score(students, subject)
        print(f"Lowest {subject.capitalize()} Score: {name} with {score}")

# Function to calculate the total score for each student
def calculate_total_score(student):
    return student['math'] + student['science'] + student['history']

# Function to add total score and rank to each student
def add_total_and_rank(students):
    for student in students:
        student['total'] = calculate_total_score(student)
    
    # Sort students by total score in descending order to determine rank
    students_sorted_by_total = sorted(students, key=lambda x: x['total'], reverse=True)
    for rank, student in enumerate(students_sorted_by_total, start=1):
        student['rank'] = rank
    
    return students_sorted_by_total

# Function to identify failing students
def failing_students(students):
    return [student['name'] for student in students if min(student['math'], student['science'], student['history']) < 40]

def print_failing_students(students):
    fails = failing_students(students)
    print(f"Failing Students: {', '.join(fails) if fails else 'None'}")

# Function to calculate percentage score for each student
def calculate_percentage(student):
    total_possible = 300  # Assuming each subject is out of 100
    return (student['total'] / total_possible) * 100

def print_student_percentages(students):
    for student in students:
        print(f"{student['name']}: {calculate_percentage(student):.2f}%")

# Function to get the top N students based on total score
def top_n_students(students, n):
    return students[:n]

def print_top_n_students(students, n=5):
    top_students = top_n_students(students, n)
    print(f"\nTop {n} Students:")
    for student in top_students:
        print(f"{student['name']} with total {student['total']}")

# Function to analyze subject-wise distribution (e.g., number of students scoring in various ranges)
def subject_distribution(students, subject):
    ranges = {
        '90-100': 0,
        '80-89': 0,
        '70-79': 0,
        '60-69': 0,
        '50-59': 0,
        '40-49': 0,
        'Below 40': 0
    }
    
    for student in students:
        score = student[subject]
        if score >= 90:
            ranges['90-100'] += 1
        elif score >= 80:
            ranges['80-89'] += 1
        elif score >= 70:
            ranges['70-79'] += 1
        elif score >= 60:
            ranges['60-69'] += 1
        elif score >= 50:
            ranges['50-59'] += 1
        elif score >= 40:
            ranges['40-49'] += 1
        else:
            ranges['Below 40'] += 1
    
    return ranges

def print_subject_distribution(students):
    for subject in ["math", "science", "history"]:
        distribution = subject_distribution(students, subject)
        print(f"\n{subject.capitalize()} Score Distribution:")
        for range_name, count in distribution.items():
            print(f"{range_name}: {count} students")

# Analysis options
def setup_switch_case(students):
    return {
        1: lambda: print_average_scores(students),
        2: lambda: print_highest_scores(students),
        3: lambda: print_lowest_scores(students),
        4: lambda: print_student_ranks(students),
        5: lambda: print_failing_students(students),
        6: lambda: print_student_percentages(students),
        7: lambda: print_top_n_students(students, 5),  # Example with n=5
        8: lambda: print_subject_distribution(students)
    }

# Main function to run the program
def main():
    filename = input("Enter the filename (e.g., 'data.txt'): ")
    students = read_students_from_file(filename)
    
    if not students:
        return  # Exit if no students are loaded
    
    # Add total score and rank to each student
    students = add_total_and_rank(students)
    
    # Set up the switch case for analysis options
    switch_case = setup_switch_case(students)
    
    while True:
        print("\nChoose an option:")
        print("1. Print Average Scores")
        print("2. Print Highest Scores")
        print("3. Print Lowest Scores")
        print("4. Print Student Ranks")
        print("5. Print Failing Students")
        print("6. Print Student Percentages")
        print("7. Print Top N Students")
        print("8. Print Subject-wise Distribution")
        print("0. Exit")
        
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue
        
        if choice == 0:
            print("Exiting...")
            break
        elif choice in switch_case:
            switch_case[choice]()  # Call the appropriate function
        else:
            print("Invalid choice, please try again.")

# Run the program
if __name__ == "__main__":
    main()
