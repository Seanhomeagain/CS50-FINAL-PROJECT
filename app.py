import google.generativeai as genai
import os

genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Write a story about a magic backpack.")
print(response.text)

model = genai.GenerativeModel("gemini-1.5-flash")
sample_pdf = genai.upload_file(media / "test.pdf")
response = model.generate_content(["Give me a summary of this pdf file.", sample_pdf])
print(response.text)