import streamlit as st
import pandas as pd

# Load recipe data from CSV
@st.cache_data
def load_recipe_data():
    try:
        return pd.read_csv('13k-recipes.csv', encoding='utf-8')  # Ensure proper encoding
    except UnicodeDecodeError:
        st.error("Error: Unable to read the recipe data. Please check the file encoding.")
        return pd.DataFrame()  # Return an empty DataFrame on error

data = load_recipe_data()

# Check if data is loaded correctly
if data.empty:
    st.error("The recipe data could not be loaded. Please verify the CSV file and try again.")
else:
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
        calorie_mapping = {
            "Maintain weight": 2000,
            "Mild weight loss": 1800,
            "Weight loss": 1500,
            "Weight gain": 2500,
        }
        total_calories = calorie_mapping[weight_goal]

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
        # (Exercise recommendation logic remains unchanged)
