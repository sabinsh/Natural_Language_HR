import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Natural Language HR Employee Records Query Application", layout="wide")
st.title("Natural Language HR Employee Records Query Application")

# === Input box for natural language query ===
question = st.text_input("Ask about employees:")

# === Submit button ===
if st.button("Submit"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Querying database..."):
            try:
                # Call FastAPI backend
                response = requests.post(
                    "http://127.0.0.1:8000/query",
                    json={"question": question},
                )
                response.raise_for_status()
                data = response.json()

                # Handle backend errors
                if data.get("error"):
                    st.error(f"Backend Error: {data['error']}")
                else:
                    # Display SQL
                    st.subheader("Generated SQL")
                    st.code(data.get("query", ""), language="sql")

                    # Display text output
                    st.subheader("Results (Text)")
                    st.text(data.get("results_text", "No results"))

                    # Display table output
                    results = data.get("results_table", [])
                    if results:
                        df = pd.DataFrame(results)
                        st.subheader("Results (Table)")
                        st.dataframe(df)
                    else:
                        st.info("No results returned.")

            except requests.exceptions.RequestException as e:
                st.error(f"Error querying backend: {e}")
