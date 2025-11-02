import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=GROQ_API_KEY,
)

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Explain the importance of fast language models",
#         }
#     ],
#     model="llama-3.3-70b-versatile",
# )
#
# print(chat_completion.choices[0].message.content)


client = Groq(api_key=GROQ_API_KEY)
completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "explain about the architectural design of this sculpture from aesthetic, philosophical, architectural, design and religious pov in holistic pov\n in precise manner\n"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "https://api.tasteiran.net/Files/persian-architecture-symmetry-8c62ab.jpg"
            }
          }
        ]
      }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=True,
    stop=None
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")

