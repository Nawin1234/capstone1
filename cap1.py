import streamlit as st
import google.generativeai as genai

# Configure API key securely (Set it as an environment variable)
API_KEY = "AIzaSyDAn69hpc4jYH4z3QsflRB_aazoBvPQw4g"
genai.configure(api_key=API_KEY)

# Fetch available models
try:
    available_models = [model.name for model in genai.list_models()]
    MODEL_NAME = "models/gemini-1.5-pro-latest" if "models/gemini-1.5-pro-latest" in available_models else "models/gemini-1.5-pro"
    
    if MODEL_NAME not in available_models:
        st.error(f"No supported Gemini models found. Available models: {available_models}")
        st.stop()
except Exception as e:
    st.error(f"Error fetching models: {e}")
    st.stop()

# Streamlit UI
st.set_page_config(page_title="AI Recipe Generator", page_icon="🍽️")
st.title("🍲 AI-Powered Recipe Generator")

# Sidebar for Cuisine Selection
st.sidebar.header("Settings")
cuisine_type = st.sidebar.selectbox("Choose Cuisine Type:", ["Any", "Indian", "Italian", "Chinese", "Mexican", "French"])

# Tabs for Fresh Ingredients & Leftover Food
tab1, tab2 = st.tabs(["🍎 Fresh Ingredients", "🍛 Leftover Food"])

with tab1:
    st.subheader("Create a Dish with Fresh Ingredients")
    ingredients = st.text_area("🥕 Enter ingredients (comma-separated):")

    if st.button("Generate Recipe", key="fresh_recipe"):
        if ingredients:
            with st.spinner("Cooking up your recipe..."):
                prompt = f"I have these fresh ingredients: {ingredients}. Can you suggest a detailed recipe?"
                if cuisine_type != "Any":
                    prompt += f" Make it a {cuisine_type} dish."
                
                try:
                    model = genai.GenerativeModel(model_name=MODEL_NAME)
                    response = model.generate_content(prompt)
                    
                    st.subheader("🍽️ Here's Your Recipe:")
                    st.write(response.text if hasattr(response, 'text') else "No response received. Try again.")
                except Exception as e:
                    st.error(f"Error generating recipe: {e}")
        else:
            st.warning("Please enter some ingredients.")

with tab2:
    st.subheader("Create a Dish with Leftover Food")
    leftovers = st.text_area("🍛 Enter leftover food items (comma-separated):")

    if st.button("Generate Leftover Recipe", key="leftover_recipe"):
        if leftovers:
            with st.spinner("Thinking of creative ways to reuse your leftovers..."):
                prompt = f"I have these leftover food items: {leftovers}. Can you suggest a creative dish using them?"
                if cuisine_type != "Any":
                    prompt += f" Make it a {cuisine_type} dish."
                
                try:
                    model = genai.GenerativeModel(model_name=MODEL_NAME)
                    response = model.generate_content(prompt)
                    
                    st.subheader("♻️ Creative Leftover Dish:")
                    st.write(response.text if hasattr(response, 'text') else "No response received. Try again.")
                except Exception as e:
                    st.error(f"Error generating recipe: {e}")
        else:
            st.warning("Please enter leftover food items.")

# Footer
st.markdown("---")
st.markdown("🔹 Built with ❤️ using Streamlit & Google Gemini AI")
