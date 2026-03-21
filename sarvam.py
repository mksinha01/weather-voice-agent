from sarvamai import 
from dotenv import load_dotenv
load_dotenv()

client = SarvamAI(
    load_dotenv()
)

response = client.text.translate(
    input="Hi, My Name is Vinayak.",
    source_language_code="auto",
    target_language_code="gu-IN",
    speaker_gender="Male"
)

print(response)
