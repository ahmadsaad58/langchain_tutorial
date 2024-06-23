# Using open AI client to read a PDF  -- https://medium.com/@erik-kokalj/effectively-analyze-pdfs-with-gpt-4o-api-378bd0f6be03

from openai import OpenAI
from openai.types.beta.threads.message_create_params import Attachment, AttachmentToolFileSearch

# file that we are working with
# this file is a chart note
TEST_FILE = 'data/patient_1.pdf'

# create client
client = OpenAI()


file = client.files.create(
	file=open(TEST_FILE, 'rb'), 
	purpose='assistants'
)

# create thread 
thread = client.beta.threads.create()


# create or fetch assistant
def get_assistant():
    for assistant in client.beta.assistants.list():
        if assistant.name == 'My Assistant Name':
            return assistant

    # No Assistant found, create a new one
    return client.beta.assistants.create(
        model='gpt-4o',
        description='You are a PDF retrieval assistant.',
        instructions="You are a helpful assistant designed to output as text. Find information from the text and files provided.",
        tools=[{"type": "file_search"}],
        # response_format={"type": "json_object"}, # Isn't possible with "file_search"
        name='My Assistant Name',
    )


# Add your prompt here
prompt = "You are a doctor who needs to analyze this input and summarize the patient's information in technical terms."
client.beta.threads.messages.create(
    thread_id = thread.id,
    role='user',
    content=prompt,
    attachments=[Attachment(file_id=file.id, tools=[AttachmentToolFileSearch(type='file_search')])]
)

print('running')

# Run the created thread with the assistant. It will wait until the message is processed.
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=get_assistant().id,
    timeout=300, # 5 minutes
    # response_format={"type": "json_object"}, # Isn't possible
)

# Eg. issue with openai server
if run.status != "completed":
    print('error')
    raise Exception('Run failed:', run.status)


# Fetch outputs of the thread
messages_cursor = client.beta.threads.messages.list(thread_id=thread.id)
messages = [message for message in messages_cursor]

message = messages[0] # This is the output from the Assistant (second message is your message)
assert message.content[0].type == "text"

# Output text of the Assistant
res_txt = message.content[0].text.value

print(res_txt)







# Delete the file(s) afterward to preserve space (max 100gb/company)
delete_ok = client.files.delete(file.id)





