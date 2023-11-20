import json

# Function to load questions from the data file
def load_questions():
    try:
        with open("data.txt", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    return data

# Function to save questions to the data file
def save_questions(questions):
    with open("data.txt", "w") as file:
        json.dump(questions, file, indent=4)

# Function to add a new question
def add_question(questions):
    print('Both options should be phrased to follow "Would you rather..." ')
    option1 = input_something("Enter Option 1: ")
    option2 = input_something("Enter Option 2: ")
    is_child_friendly = input_bool("Is this question appropriate for children? (Y/N): ")

    new_question = {
        "option_1": option1,
        "option_2": option2,
        "children": is_child_friendly,
        "votes_1": 0,
        "votes_2": 0,
        "likes": 0,
        "dislikes": 0
    }
    questions.append(new_question)
    save_questions(questions)
    print("Question added.\n")

# Function to list all questions
def list_questions(questions):
    if not questions:
        print("No questions saved.")
    else:
        print('List of questions')
        for i, question in enumerate(questions, start=1):
            option1 = question['option_1']
            option2 = question['option_2']
            print(f"  {i}) {option1} / {option2}")

# Function to delete a question
def delete_question(questions, question_number):
    if 1 <= question_number <= len(questions):
        deleted_question = questions.pop(question_number - 1)
        save_questions(questions)
        print("Question deleted.")
    else:
        print("Invalid question number.")

# Function for input validation
def input_something(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")

# Function for boolean input validation
def input_bool(prompt):
    while True:
        value = input(prompt).strip().lower()
        if value in ["y", "n"]:
            return value == "y"
        print("Invalid input. Please enter 'Y' for Yes or 'N' for No.")

# Function for integer input validation
def input_int(prompt):
    while True:
        value = input(prompt)
        if value.isdigit():
            return int(value)
        print("Invalid input. Please enter a valid integer.")

# Function to search questions
def search_questions(questions, search_term):
    results = []
    for i, question in enumerate(questions, start=1):
        if search_term.lower() in question['option_1'].lower() or search_term.lower() in question['option_2'].lower():
            results.append((i, question))

    return results

# Function to view a question
def view_question(questions, question_number):
    if not questions:
        print("No questions saved.")
        return

    if 1 <= question_number <= len(questions):
        question = questions[question_number - 1]
        option1 = question['option_1'] + "?"
        option2 = question['option_2'] + "?"
        children = "This question is not appropriate for children!" if not question['children'] else "This question is suitable for children."

        votes1 = question['votes_1']
        votes2 = question['votes_2']
        likes = question['likes']
        dislikes = question['dislikes']

        print("Would you rather…")
        print(f"  Option 1) {option1}")
        print(f"  Option 2) {option2}")
        print()
        print(children)
        print(f"Option 1 has received {votes1} vote(s), Option 2 has received {votes2} vote(s).")
        print(f"This question has received {likes} like(s) and {dislikes} dislike(s).")
    else:
        print("Invalid question number.")

# Main program
if __name__ == "__main__":
    questions = load_questions()

    print()
    print("Welcome to the 'Would You Rather' Admin Program.")
    print()

    while True:
        print("Choose [a]dd, [l]ist, [s]earch, [v]iew, [d]elete or [q]uit.")
        choice = input("> ").lower()

        if choice == "a":
            add_question(questions)
            # print()
        elif choice == "l":
            list_questions(questions)
            print()
        elif choice == "s":
            search_term = input_something("Enter search term: ")
            search_results = search_questions(questions, search_term)
            if search_results:
                print("Search results:")
                for result in search_results:
                    question_number, question = result
                    option1 = question['option_1']
                    option2 = question['option_2']

                    print(f"  {question_number}) {option1} / {option2}")
                    print()
            else:
                print("No results found.")
                print()
        elif choice == "v":
            question_number = input_int("Question number to view: ")
            view_question(questions, question_number)
            print()
        elif choice == "d":
            list_questions(questions)
            question_number = input_int("Question number to delete: ")
            delete_question(questions, question_number)
            print()
        elif choice == "q":
            print("Goodbye!")
            print()
            break
        else:
            print("Invalid choice. Please try again.")
