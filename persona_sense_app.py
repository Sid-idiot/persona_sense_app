import streamlit as st
import google.generativeai as genai

# Replace with your actual Gemini API key
GEMINI_API_KEY = "AIzaSyBEliZKoO2qyJNdZHr-O4YrpmXYyGhKDwY"

# Sample questions for the Big Five personality traits
questions = [
    {"text": "I'm excited to try new activities at school.", "trait": "O", "scoring": "+"},
    {"text": "I like thinking deeply about things I learn in class.", "trait": "O", "scoring": "+"},
    {"text": "I often come up with creative ideas for projects.", "trait": "O", "scoring": "+"},
    {"text": "I prefer classes with practical assignments.", "trait": "O", "scoring": "-"},
    {"text": "I prefer a regular school routine.", "trait": "O", "scoring": "-"},
    {"text": "I enjoy visiting art exhibits or shows.", "trait": "O", "scoring": "+"},
    {"text": "I like working on challenging assignments.", "trait": "O", "scoring": "+"},
    {"text": "I always have my schoolwork ready on time.", "trait": "C", "scoring": "+"},
    {"text": "I start studying for tests early.", "trait": "C", "scoring": "+"},
    {"text": "I am very thorough in my schoolwork.", "trait": "C", "scoring": "+"},
    {"text": "My locker is usually messy.", "trait": "C", "scoring": "-"},
    {"text": "I often misplace things I need for class.", "trait": "C", "scoring": "-"},
    {"text": "I avoid doing my homework.", "trait": "C", "scoring": "-"},
    {"text": "I wait until the last minute to start projects.", "trait": "C", "scoring": "-"},
    {"text": "I look forward to spending time with friends.", "trait": "E", "scoring": "+"},
    {"text": "I find it easy to connect with people at school.", "trait": "E", "scoring": "+"},
    {"text": "I don't express my thoughts very often.", "trait": "E", "scoring": "-"},
    {"text": "I prefer to listen rather than speak in class.", "trait": "E", "scoring": "-"},
    {"text": "I chat a lot with people at school.", "trait": "E", "scoring": "+"},
    {"text": "I like to take charge in group projects.", "trait": "E", "scoring": "+"},
    {"text": "I'm usually quiet in large gatherings.", "trait": "E", "scoring": "-"},
    {"text": "I'm willing to help classmates with their work.", "trait": "A", "scoring": "+"},
    {"text": "I'm kind to people who are having a hard time.", "trait": "A", "scoring": "+"},
    {"text": "I try to understand my friends' feelings.", "trait": "A", "scoring": "+"},
    {"text": "I have been known to be competitive to others.", "trait": "A", "scoring": "-"},
    {"text": "I sometimes say unkind things to people.", "trait": "A", "scoring": "-"},
    {"text": "I don't always think about how my words affect others.", "trait": "A", "scoring": "-"},
    {"text": "I can be mean to others.", "trait": "A", "scoring": "-"},
    {"text": "I feel anxious about tests.", "trait": "N", "scoring": "+"},
    {"text": "I worry about my grades.", "trait": "N", "scoring": "+"},
    {"text": "I get overwhelmed by a lot of homework.", "trait": "N", "scoring": "+"},
    {"text": "I feel confident in myself at school.", "trait": "N", "scoring": "-"},
    {"text": "I don't get stressed out by deadlines.", "trait": "N", "scoring": "-"},
    {"text": "I rarely feel sad about school.", "trait": "N", "scoring": "-"},
    {"text": "I get frustrated when I don't understand something.", "trait": "N", "scoring": "+"},
]

questions_by_trait = {
    "Openness": [q for q in questions if q["trait"] == "O"],
    "Conscientiousness": [q for q in questions if q["trait"] == "C"],
    "Extraversion": [q for q in questions if q["trait"] == "E"],
    "Agreeableness": [q for q in questions if q["trait"] == "A"],
    "Neuroticism": [q for q in questions if q["trait"] == "N"],
}

response_options = ["1 (Strongly Disagree)", "2 (Disagree)", "3 (Neutral)", "4 (Agree)", "5 (Strongly Agree)"]

def calculate_scores(responses, all_questions):
    trait_scores = {
        "O": 0,
        "C": 0,
        "E": 0,
        "A": 0,
        "N": 0,
    }
    trait_counts = {
        "O": 0,
        "C": 0,
        "E": 0,
        "A": 0,
        "N": 0,
    }

    response_values = {
        "1 (Strongly Disagree)": 1,
        "2 (Disagree)": 2,
        "3 (Neutral)": 3,
        "4 (Agree)": 4,
        "5 (Strongly Agree)": 5,
    }

    for question_data in all_questions:
        text = question_data["text"]
        trait = question_data["trait"]
        scoring = question_data["scoring"]

        if text in responses:
            raw_score = response_values[responses[text]]
            if scoring == "-":
                reversed_score = 6 - raw_score  # Reverse scoring
                trait_scores[trait] += reversed_score
            else:
                trait_scores[trait] += raw_score
            trait_counts[trait] += 1

    average_scores = {}
    for trait, total_score in trait_scores.items():
        if trait_counts[trait] > 0:
            average_scores[trait] = total_score / trait_counts[trait]
        else:
            average_scores[trait] = 0

    return average_scores

# Streamlit interface
st.set_page_config(page_title="Persona_Sense", layout="wide")
st.title("Persona_Sense")

# Creating a 3-column layout
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Personality Test")
    test_button = st.button("Start Personality Test")
    
    if test_button:
        st.session_state.page = "test_page"

if 'page' not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "test_page":
    st.header("Know Yourself")
    st.write("Please answer the following questions:")

    if 'responses' not in st.session_state:
        st.session_state['responses'] = {}

    # Section for Openness
    st.header("Openness")
    for i, q in enumerate(questions_by_trait["Openness"]):
        key = f"O_{i}"
        response = st.radio(q["text"], response_options, key=key)
        st.session_state['responses'][q["text"]] = response

    # Section for Conscientiousness
    st.header("Conscientiousness")
    for i, q in enumerate(questions_by_trait["Conscientiousness"]):
        key = f"C_{i}"
        response = st.radio(q["text"], response_options, key=key)
        st.session_state['responses'][q["text"]] = response

    # Section for Extraversion
    st.header("Extraversion")
    for i, q in enumerate(questions_by_trait["Extraversion"]):
        key = f"E_{i}"
        response = st.radio(q["text"], response_options, key=key)
        st.session_state['responses'][q["text"]] = response

    # Section for Agreeableness
    st.header("Agreeableness")
    for i, q in enumerate(questions_by_trait["Agreeableness"]):
        key = f"A_{i}"
        response = st.radio(q["text"], response_options, key=key)
        st.session_state['responses'][q["text"]] = response

    # Section for Neuroticism
    st.header("Neuroticism")
    for i, q in enumerate(questions_by_trait["Neuroticism"]):
        key = f"N_{i}"
        response = st.radio(q["text"], response_options, key=key)
        st.session_state['responses'][q["text"]] = response

    submit_button = st.button("Submit Answers")
    if submit_button:
        calculated_scores = calculate_scores(st.session_state['responses'], questions)
        st.write("Thank you for completing the questionnaire!")
        st.write("Your personality scores:")
        st.write(calculated_scores)

        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel(model_name='gemini-1.5-pro')
            response = model.generate_content(
                contents=[{"text": "Your personality traits are: " + str(calculated_scores)}]
            )
            st.subheader("Personality Analysis and Feedback:")
            st.write(response.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")


