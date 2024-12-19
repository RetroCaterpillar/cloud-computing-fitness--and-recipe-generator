import streamlit as st
import pandas as pd

# Load recipe data from CSV
@st.cache_data
def load_recipe_data():
    return pd.read_csv('13k-recipes.csv')

data = load_recipe_data()

# Add an image at the top for a professional look
st.image("mealplan.jpg", use_container_width=True, caption="Your Personalized Meal Planner")

# Main Title
st.title("Easy Meal Planning App")

# Tabs for navigation
tab1, tab2, tab3 = st.tabs(["Diet Recommendation", "Recipe Recommendation", "Exercise Recommendation"])

# -------------------- TAB 1: Diet Recommendation --------------------
with tab1:
    st.header("Automatic Diet Recommendation")

    # Input fields
    age = st.number_input("Age", min_value=1, max_value=100, value=25)
    height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170)
    weight = st.number_input("Weight (kg)", min_value=10, max_value=300, value=70)

    gender = st.radio("Gender", options=["Male", "Female"])
    activity = st.selectbox(
        "Activity Level",
        [
            "Little/no exercise",
            "Light exercise",
            "Moderate exercise",
            "Heavy exercise",
            "Extra active",
        ],
    )

    meals_per_day = st.slider("Meals per day", min_value=1, max_value=6, value=3)
    weight_goal = st.selectbox(
        "Choose your weight goal:",
        ["Maintain weight", "Mild weight loss", "Weight loss", "Weight gain"],
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

    # Calorie Recommendation Logic
    st.subheader("Calories Calculator")
    st.write("Results for maintaining, losing, or gaining weight:")

    # Calorie logic
    if weight_goal == "Maintain weight":
        total_calories = 2000
    elif weight_goal == "Mild weight loss":
        total_calories = 1800
    elif weight_goal == "Weight loss":
        total_calories = 1500
    elif weight_goal == "Weight gain":
        total_calories = 2500

    st.write(f"**Daily Calorie Target:** {total_calories} Calories/day")

    # Split calories for meals
    morning_calories = int(total_calories * 0.3)
    evening_calories = int(total_calories * 0.3)
    dinner_calories = int(total_calories * 0.4)

    st.write(f"**Morning Calories:** {morning_calories}")
    st.write(f"**Evening Calories:** {evening_calories}")
    st.write(f"**Dinner Calories:** {dinner_calories}")

    # Generate Recipes Feature
    if st.button("Generate Recipes"):
        st.subheader("Recommended Recipes:")

        # Generate random recipes for each meal
        morning_recipes = data['Title'].sample(3).tolist()
        evening_recipes = data['Title'].sample(3).tolist()
        dinner_recipes = data['Title'].sample(3).tolist()

        # Display generated recipe titles
        st.write("🍳 **Morning Recipes:**")
        for recipe in morning_recipes:
            st.write(f"- {recipe}")

        st.write("🌇 **Evening Recipes:**")
        for recipe in evening_recipes:
            st.write(f"- {recipe}")

        st.write("🌙 **Dinner Recipes:**")
        for recipe in dinner_recipes:
            st.write(f"- {recipe}")

# -------------------- TAB 2: Recipe Recommendation --------------------
with tab2:
    st.header("Recipe Recommendation")

    # Search Recipes by Name
    st.subheader("🔍 Search Recipe by Name")
    recipe_name = st.text_input("Enter Recipe Name:")
    if recipe_name:
        matching_recipe = data[data['Title'].str.contains(recipe_name, case=False, na=False)]
        if not matching_recipe.empty:
            recipe = matching_recipe.iloc[0]
            st.write(f"**Title:** {recipe['Title']}")
            st.write(f"**Ingredients:** {recipe['Ingredients']}")
            st.write(f"**Instructions:** {recipe['Instructions']}")
        else:
            st.warning("No recipe found with that name. Try another name.")

    st.write("---")

    # Search Recipes by Available Ingredients
    st.subheader("🛒 Search Recipes by Available Ingredients")
    selected_ingredients = st.text_area("Enter available ingredients (comma-separated):", "")

    if selected_ingredients:
        selected_ingredients = [ingredient.strip().lower() for ingredient in selected_ingredients.split(",")]

        # Filter recipes based on ingredients
        matching_recipes = data[
            data['Cleaned_Ingredients'].apply(
                lambda ingredients: all(ingredient in ingredients.lower() for ingredient in selected_ingredients)
            )
        ]

        # Display matching recipes
        st.subheader("Matching Recipes:")
        if not matching_recipes.empty:
            for _, recipe in matching_recipes.head(5).iterrows():  # Display up to 5 matches
                st.write(f"**Title:** {recipe['Title']}")
                st.write("---")
        else:
            st.warning("No recipes found with the selected ingredients. Try different ingredients.")

# -------------------- TAB 3: Exercise Recommendation --------------------
with tab3:
    st.header("Exercise Recommendation")

    # Input fields for exercise recommendations
    age = st.number_input("Age", min_value=1, max_value=100, value=25, key="exercise_age")
    height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170, key="exercise_height")
    weight = st.number_input("Weight (kg)", min_value=10, max_value=300, value=70, key="exercise_weight")

    gender = st.radio("Gender", options=["Male", "Female"], key="exercise_gender")
    activity_level = st.selectbox(
        "Activity Level",
        ["Little/no exercise", "Light exercise", "Moderate exercise", "Heavy exercise", "Extra active"],
        key="exercise_activity"
    )

    weight_goal = st.selectbox(
        "Choose your weight goal:",
        ["Maintain weight", "Mild weight loss", "Weight loss", "Weight gain"],
        key="exercise_weight_goal"
    )

    # BMI Calculation
    bmi = weight / ((height / 100) ** 2)
    st.subheader("BMI Calculator")
    st.write(f"**Body Mass Index (BMI):** {bmi:.1f} kg/m²")

    if bmi < 18.5:
        st.success("You are underweight. Light exercises recommended.")
    elif 18.5 <= bmi < 24.9:
        st.success("Your weight is normal. Stay active!")
    elif 25 <= bmi < 29.9:
        st.warning("You are overweight. Start a fitness routine.")
    else:
        st.error("You are obese. Exercises are highly recommended.")

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

    # Button to generate exercises based on fitness level
    if st.button("Generate Exercises"):
        # Generate exercises based on user fitness level
        morning_exercises, evening_exercises = generate_exercise_recommendation(age, weight_goal, activity_level)

        # Display exercises for morning and evening
        if morning_exercises:
            st.write("**Morning Exercises:**")
            for exercise in morning_exercises:
                st.write(f"- {exercise}")
        
        if evening_exercises:
            st.write("**Evening Exercises:**")
            for exercise in evening_exercises:
                st.write(f"- {exercise}")
