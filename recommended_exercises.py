import streamlit as st

# Function to generate exercise recommendations based on user inputs
def generate_exercise_recommendation(age, weight_goal, activity_level):
    exercises = {
        "Little/no exercise": [
            "5-minute walk",
            "Stretching",
            "Basic Yoga poses"
        ],
        "Light exercise": [
            "10-minute walk",
            "Push-ups (3 sets of 10)",
            "Basic Yoga poses"
        ],
        "Moderate exercise": [
            "20-minute jogging",
            "Push-ups (3 sets of 20)",
            "Bodyweight squats (3 sets of 15)"
        ],
        "Heavy exercise": [
            "30-minute cycling",
            "Push-ups (3 sets of 30)",
            "Lunges (3 sets of 20)"
        ],
        "Extra active": [
            "45-minute cycling or running",
            "Push-ups (3 sets of 40)",
            "Lunges (3 sets of 30)",
            "Planks (3 sets of 30 seconds)"
        ]
    }

    # Recommend exercises based on activity level
    if activity_level in exercises:
        morning_exercises = exercises[activity_level][:2]  # Morning workout (first two)
        evening_exercises = exercises[activity_level][2:]  # Evening workout (next exercises)

        # Add specific exercises for weight goal
        if weight_goal == "Mild weight loss":
            evening_exercises.append("10-minute cardio")
        elif weight_goal == "Weight loss":
            evening_exercises.append("15-minute cardio")
        elif weight_goal == "Weight gain":
            morning_exercises.append("Light strength training (e.g., resistance bands)")
        
        return morning_exercises, evening_exercises
    else:
        return [], []  # Return empty lists if no valid activity level is found

# App title
st.title("Exercise Recommendation App")

# Input fields for user information
age = st.number_input("Age", min_value=1, max_value=100, value=25)
height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170)
weight = st.number_input("Weight (kg)", min_value=10, max_value=300, value=70)

gender = st.radio("Gender", options=["Male", "Female"])
activity_level = st.selectbox(
    "Activity Level",
    [
        "Little/no exercise",
        "Light exercise",
        "Moderate exercise",
        "Heavy exercise",
        "Extra active",
    ]
)
weight_goal = st.selectbox(
    "Choose your weight goal:",
    ["Maintain weight", "Mild weight loss", "Weight loss", "Weight gain"]
)

# BMI Calculation
bmi = weight / ((height / 100) ** 2)
st.subheader("BMI Calculator")
st.write(f"**Body Mass Index (BMI):** {bmi:.1f} kg/m²")

if bmi < 18.5:
    st.error("Underweight")
elif 18.5 <= bmi < 24.9:
    st.success("Normal weight")
elif 25 <= bmi < 29.9:
    st.warning("Overweight")
else:
    st.error("Obesity")

# Fitness Level Determination
fitness_level = "fit" if bmi >= 24.9 or activity_level in ["Moderate exercise", "Heavy exercise", "Extra active"] else "not fit"

# Button to generate exercises based on fitness level
if st.button("Generate Exercises"):
    if fitness_level == "fit":
        st.subheader("Exercise Recommendation for Fit Individuals:")
        # Light exercise for fit individuals
        morning_exercises, evening_exercises = generate_exercise_recommendation(age, weight_goal, "Light exercise")
    else:
        st.subheader("Exercise Recommendation for Not-So-Fit Individuals:")
        # Heavy exercise for not fit individuals
        morning_exercises, evening_exercises = generate_exercise_recommendation(age, weight_goal, "Heavy exercise")

    # Display exercises for morning and evening
    if morning_exercises:
        st.write("**Morning Exercises:**")
        for exercise in morning_exercises:
            st.write(f"- {exercise}")
    
    if evening_exercises:
        st.write("**Evening Exercises:**")
        for exercise in evening_exercises:
            st.write(f"- {exercise}")
