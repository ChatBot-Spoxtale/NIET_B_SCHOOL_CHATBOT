from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
# print(genai.Client(api_key=os.getenv("GOOGLE_API_KEY")))
response = client.models.generate_content(
    model="gemini-flash-latest",
    contents="tell me about virat kholi"
)

print(response.text)

# from google import genai
# import os
# from dotenv import load_dotenv

# load_dotenv()

# client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# models = client.models.list()

# for m in models:
#     print(m.name, m.supported_generation_methods)

# from google import genai
# import os
# from dotenv import load_dotenv

# load_dotenv()

# client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# models = client.models.list()

# for m in models:
#     print(m.name)
