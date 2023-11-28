from openai import OpenAI
import streamlit as st
from htmlTemplates import bot_template, user_template, css
import json
import time


def get_message_from_json(obj):
    json_returned = json.loads(obj.model_dump_json())
    message = json_returned["data"][0]["content"][0]["text"]["value"]
    return message


def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


if __name__ == "__main__":
    client = OpenAI()
    assistant_id = "asst_9JuJxQc2y1LB8rjIVwtUifs6"
    thread = client.beta.threads.create()
    st.set_page_config(page_title="CZAT DŻIPITI", page_icon="🏠")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Zadaj pytanie"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        with st.spinner("Piszę ..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=prompt,
            )
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant_id,
            )
            run = wait_on_run(run, thread)
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            returned_message = get_message_from_json(messages)
            response = returned_message
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
