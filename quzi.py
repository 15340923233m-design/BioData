import streamlit as st

# Page title
st.title("📚 Streamlit Quiz App")

# Correct answers (you can change them)
correct_answers = {
    "q1": "Python",
    "q2": "Guido van Rossum",
    "q3": "st.button()"
}

# Question 1
st.subheader("Question 1")
q1 = st.radio(
    "Which programming language is Streamlit built with?",
    ["Java", "Python", "JavaScript", "C++"]
)
st.divider()

# Question 2
st.subheader("Question 2")
q2 = st.radio(
    "Who created Python?",
    ["Elon Musk", "Guido van Rossum", "Bill Gates", "Mark Zuckerberg"]
)
st.divider()

# Question 3
st.subheader("Question 3")
q3 = st.radio(
    "Which Streamlit widget is used for a clickable button?",
    ["st.text()", "st.button()", "st.slider()", "st.image()"]
)
st.divider()

# Submit button
if st.button("Submit Answers"):
    score = 0

    # Check Q1
    if q1 == correct_answers["q1"]:
        st.success("Question 1: Correct! ✅")
        score += 1
    else:
        st.error(f"Question 1: Wrong! Correct answer: {correct_answers['q1']} ❌")

    # Check Q2
    if q2 == correct_answers["q2"]:
        st.success("Question 2: Correct! ✅")
        score += 1
    else:
        st.error(f"Question 2: Wrong! Correct answer: {correct_answers['q2']} ❌")

    # Check Q3
    if q3 == correct_answers["q3"]:
        st.success("Question 3: Correct! ✅")
        score += 1
    else:
        st.error(f"Question 3: Wrong! Correct answer: {correct_answers['q3']} ❌")

    # Show final score
    st.subheader(f"🏆 Your Total Score: {score}/3")