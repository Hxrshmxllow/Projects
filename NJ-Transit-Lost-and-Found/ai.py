import base64
from openai import OpenAI

client = OpenAI(api_key='sk-75ippQsXjIhFJG1eanGzd2ywJIhNKSAl0Uh7q-m-nUT3BlbkFJvZyRIyiMHNiq1V97fMiegsRlp6k30E1ImctF-ysaYA')

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def get_imageDes(image_path):
   base64_image = encode_image(image_path)
   response = client.chat.completions.create(
     model="gpt-4o-mini",
     messages=[
       {
         "role":"user",
         "content" : 
         [
           {
             "type" : "text",
             "text" : "What is in this image, explain it using keywords? And in answer I don't want you to mention the term KeyWord",
           },
           {
             "type" : "image_url",
             "image_url" : 
             {
               "url" : f"data:image/jpeg;base64,{base64_image}"
             },
           },
         ],
        }
     ],
    )
   return response.choices[0].message.content