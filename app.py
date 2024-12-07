from openai import OpenAI
import streamlit as st



# Add a sidebar for LangChain
st.sidebar.title("ChatGPT-like clone")


# Add a dropdown for model selection
model_options = ["gpt-4o", "gpt-4o-mini", "o1-mini", "o1-preview"]
selected_model = st.sidebar.selectbox("OpenAI model:", model_options)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = selected_model

# Update the model if the user changes the selection
if st.session_state["openai_model"] != selected_model:
    st.session_state["openai_model"] = selected_model


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Anything in mind?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})