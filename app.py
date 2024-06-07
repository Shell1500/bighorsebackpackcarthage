import streamlit as st
import pandas as pd
import random



TITLE = "MCQ STYLE QUIZ"



# Load CSV files
def load_questions(file_path):
    return pd.read_csv(file_path, header=None, skiprows=1)

# Select random questions
def select_questions(df, num_questions):
    return df.sample(num_questions)

# Main function
def main():
    st.title(TITLE)

    # Load the questions from the CSV files
    general_df = load_questions('general.csv')
    specific_df = load_questions('specific.csv')

    # Initialize session state variables if they don't exist
    if 'questions' not in st.session_state:
        general_questions = select_questions(general_df, 2)
        specific_questions = select_questions(specific_df, 5)
        st.session_state.questions = pd.concat([general_questions, specific_questions]).sample(frac=1).reset_index(drop=True)

    if 'score' not in st.session_state:
        st.session_state.score = 0
        
    if 'responses' not in st.session_state:
        st.session_state.responses = [None] * len(st.session_state.questions)
        
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    all_questions = st.session_state.questions

    # Create a form for the quiz
    with st.form(key='quiz_form'):
        for idx, row in all_questions.iterrows():
            st.write(f"### Question {idx + 1}")
            st.write(row[0])  # Question

            options = [row[1], row[2], row[3], row[4]]
            st.session_state.responses[idx] = st.radio(f"Select an option for Question {idx + 1}:", 
                                                       options, 
                                                       key=f"q{idx}",
                                                       index=None)

        # Check if all questions are answered
        all_answered = all(response is not None for response in st.session_state.responses)
        
        # Add an alert if not all questions are answered
        if not all_answered:
            st.warning("Please answer all questions before submitting.")


        submit_button = st.form_submit_button(label='Submit Quiz')

    # Process form submission
    if submit_button and all_answered and not st.session_state.submitted:
        st.session_state.score = 0
        st.session_state.submitted = True
        for idx, row in all_questions.iterrows():
            correct_answer = row[ord(row[5])-64]
            user_response = st.session_state.responses[idx]
            if user_response == correct_answer:
                st.session_state.score += 1
                st.success(row[6])
            else:
                st.error(f"Question {idx + 1}: {row[7]}")  # Incorrect answer response

        st.write(f"## Your Score: {st.session_state.score} / 7")

if __name__ == "__main__":
    main()
