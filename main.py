from openai import OpenAI
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

    user_input = input("\nPytanie: ")
    while user_input != "q":
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input,
        )
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id,
        )
        run = wait_on_run(run, thread)
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        returned_message = get_message_from_json(messages)
        print("Odpowiedź: " + returned_message)
        user_input = input("\nPytanie: ")
