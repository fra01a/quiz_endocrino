import random
import streamlit as st
import docx

# Function to read questions from docx file
def read_questions_from_docx(file_path):
    doc = docx.Document(file_path)
    questions = []
    current_question = None

    for para in doc.paragraphs:
        text = para.text.strip()
        if len(text) > 1 and text[0].isdigit() and text[1] == '.':
            if current_question:
                questions.append(current_question)
            current_question = {"question": text, "answers": [], "correct": None}
        elif text.startswith("a)") or text.startswith("b)") or text.startswith("c)") or text.startswith("d)") or text.startswith("e)"):
            if current_question:
                current_question["answers"].append(text)
                if text.startswith("a)"):  # Assuming the first option is always the correct one
                    current_question["correct"] = len(current_question["answers"]) - 1
    if current_question:
        questions.append(current_question)
    return questions

# Function to shuffle the answers and store the shuffled order
def shuffle_answers(questions):
    for question in questions:
        correct_answer = question["answers"][question["correct"]]
        shuffled_order = list(range(len(question["answers"])))
        random.shuffle(shuffled_order)
        question["shuffled_order"] = shuffled_order
        question["shuffled_answers"] = [question["answers"][i] for i in shuffled_order]
        question["correct"] = shuffled_order.index(question["correct"])  # Find the new position of the correct answer
    return questions

# Percorso del file con le domande
file_path = 'Domandendocrino.docx'
questions = read_questions_from_docx(file_path)
shuffled_questions = shuffle_answers(questions)

# Streamlit app
def main():
    st.title("Quiz Game")

    if 'score' not in st.session_state:
        st.session_state.score = 0
        st.session_state.current_question_index = 0
        st.session_state.answers = [None] * len(shuffled_questions)
        st.session_state.show_feedback = False
        st.session_state.shuffled_questions = shuffled_questions

    if st.session_state.current_question_index < len(st.session_state.shuffled_questions):
        question = st.session_state.shuffled_questions[st.session_state.current_question_index]
        st.write(f"Q{st.session_state.current_question_index + 1}: {question['question']}")

        selected_answer = st.radio(
            "Select your answer:",
            options=[(i, answer[3:]) for i, answer in enumerate(question['shuffled_answers'])],
            format_func=lambda x: x[1],
            key=f"question_{st.session_state.current_question_index}"
        )

        if selected_answer is not None:
            st.session_state.answers[st.session_state.current_question_index] = selected_answer[0]

        if st.session_state.show_feedback:
            correct_answer_idx = question['correct']
            correct_answer_text = question['shuffled_answers'][correct_answer_idx][3:]
            if selected_answer is not None and selected_answer[0] == correct_answer_idx:
                st.success("Correct!")
            else:
                st.error(f"Incorrect. The correct answer is: {correct_answer_text}")

        if st.button("Next"):
            if not st.session_state.show_feedback:
                st.session_state.show_feedback = True
            else:
                st.session_state.show_feedback = False
                if selected_answer is not None and selected_answer[0] == question['correct']:
                    st.session_state.score += 1
                st.session_state.current_question_index += 1
            st.experimental_rerun()
    else:
        st.write(f"Your final score is {st.session_state.score} out of {len(st.session_state.shuffled_questions)}")
        if st.button("Restart"):
            st.session_state.score = 0
            st.session_state.current_question_index = 0
            st.session_state.answers = [None] * len(st.session_state.shuffled_questions)
            st.session_state.show_feedback = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()
