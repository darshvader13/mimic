import openai
import docx2txt
import os
import json

openai.api_key = os.getenv("api_key")

def write_jsonl(file_path, data):
    with open(file_path, 'a') as file:
        json.dump(data, file)
        file.write('\n')

def chat(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    print(response)
    return response.choices[0].message.content.strip()

def finetune():
    return None

def summarize(text):
    messages=[
        {"role": "system", "content": "You are a helpful assistant who can summarize very concisely."},
        {"role": "user", "content": 'Summarize this in one sentence starting with "This essay is about". ' + text}
    ]
    return chat(messages)

parse_summary = lambda summary: " ".join(summary.split(' ')[4:])

files = {}
summaries = {}
directory_path = 'C:/Users/dbala/Desktop/mimic/files/'
for filename in os.listdir(directory_path):
    docx_file_path = os.path.join(directory_path, filename)
    text = docx2txt.process(docx_file_path)
    files[filename] = text
    summaries[filename] = parse_summary(summarize(text))


jsonl_file = "data.jsonl"
training_messages = {}
for filename in files.keys():
    text = files[filename]
    summary = summaries[filename]

    system_message = "You are a helpful assistant with incredible mimicking abilities who can only respond in a single very specific tone, infliction, vocabulary, and style of writing, which you are being trained upon." #this needs fixing
    user_message = "Write me an essay about " + summary
    assistant_message = text

    messsages_dict = {'messages': []}
    messsages_dict['messages'] += [{'role': 'system', 'content': system_message}]
    messsages_dict['messages'] += [{'role': 'user', 'content': user_message}]
    messsages_dict['messages'] += [{'role': 'assistant', 'content': assistant_message}]
    write_jsonl(jsonl_file, messsages_dict)


training_file = openai.File.create(
  file=open(jsonl_file, "rb"),
  purpose='fine-tune'
)

print(training_file.id)
#code needs to wait on this before sending
creation_response = openai.FineTuningJob.create(training_file=training_file.id, model="gpt-3.5-turbo")
print(creation_response)
