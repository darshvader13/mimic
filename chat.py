import openai
import docx2txt
import os

api_key = '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'
openai.api_key = api_key

#l = openai.FineTuningJob.list(limit=10)
#print(l)


finetune_id ='ft:gpt-3.5-turbo-0613:personal::82BdTRpR'
finetune_id2 = 'ft:gpt-3.5-turbo-0613:personal::7zZ1fnik'

response = openai.ChatCompletion.create(
  model=finetune_id,
  messages=[
    {"role": "system", "content": "You are a helpful assistant who can only respond in the very specific tone, infliction, vocabulary, and style of writing that you were trained upon."},
    {"role": "user", "content": "Write me a three paragraph essay about how the role of technology in George Orwell's 1984."}
  ]
)
choice = response.choices[0].message.content.strip()
print(choice)


#id = 'file-XFFs3cxOWPIFaXloX8KA3DY3'
#openai.FineTuningJob.create(training_file=id, model="gpt-3.5-turbo")


'''
directory_path = 'C:/Users/dbala/Desktop/mimic/files/'
for filename in os.listdir(directory_path):
    if "buddhism" in filename:
        docx_file_path = os.path.join(directory_path, filename)
        text = docx2txt.process(docx_file_path)
        sentences = sent_tokenize(text)
        print(sentences[:5])
'''




