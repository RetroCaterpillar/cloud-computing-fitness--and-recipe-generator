import streamlit as st
import pandas as pd

# Load recipe data from CSV
@st.cache_data
def load_recipe_data():
    return pd.read_csv('13k-recipes.csv')

data = load_recipe_data()

# App title
st.title("Custom Food Recommendation")

# -------------------- Search Recipe by Name --------------------
st.header("Find Recipe by Name")

# Input recipe name
recipe_name = st.text_input("Enter a recipe name:")

if recipe_name:
    # Search for the recipe
    matching_recipe = data[data['Title'].str.lower() == recipe_name.strip().lower()]

    # Display full ingredients and instructions
    if not matching_recipe.empty:
        st.subheader("Recipe Details:")
        recipe = matching_recipe.iloc[0]
        st.write(f"**Title:** {recipe['Title']}")
        st.write(f"**Ingredients:** {recipe['Ingredients']}")
        st.write(f"**Instructions:** {recipe['Instructions']}")
    else:
        st.warning("Recipe not found. Please try another name.")

# -------------------- Recommend Recipe Based on Available Ingredients --------------------
st.header("Find Recipes Based on Available Ingredients")

# Input available ingredients
available_ingredients = st.text_area("List your available ingredients (comma-separated):")

if available_ingredients:
    available_ingredients = [
        ingredient.strip().lower() for ingredient in available_ingredients.split(",")
    ]

    # Filter recipes containing any of the available ingredients
    matching_recipes = data[
        data['Cleaned_Ingredients'].apply(
            lambda ingredients: any(ingredient in ingredients.lower() for ingredient in available_ingredients)
        )
    ]

    # Display results
    st.subheader("Recommended Recipes:")
    if not matching_recipes.empty:
        for _, recipe in matching_recipes.head(5).iterrows():  # Display up to 5 matches
            st.write(f"**Title:** {recipe['Title']}")
            st.write(f"**Ingredients:** {recipe['Ingredients']}")
            st.write(f"**Instructions:** {recipe['Instructions']}")
            st.write("---")
    else:
        st.warning("No matching recipes found. Please try different ingredients.")
