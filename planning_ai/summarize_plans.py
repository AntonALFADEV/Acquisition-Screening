import fitz  # PyMuPDF
import openai
import os

# Sørg for at have din OpenAI-nøgle som en environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")


def read_pdf_text(file):
    """Læs hele teksten fra en PDF ved brug af PyMuPDF"""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def summarize_pdf(file):
    """AI-baseret opsummering af PDF med OpenAI's GPT-4"""
    raw_text = read_pdf_text(file)

    # Evt. klip meget lange PDF'er ned for at spare tokens
    max_chars = 8000
    trimmed_text = raw_text[:max_chars]

    prompt = f"""
Du er en AI-assistent, der hjælper med at analysere danske lokal- og kommuneplaner.

Opsummer følgende planuddrag kort og præcist. Fokuser især på:
- Hvad området må anvendes til (bolig, erhverv, etc.)
- Etageantal, bebyggelsesprocent og højde
- Zonestatus (byzone, landzone mv.)
- Eventuelle begrænsninger eller krav

Tekst:
{trimmed_text}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Du er ekspert i byplanlægning og lokalplaner."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        summary = response.choices[0].message.content
        return summary

    except Exception as e:
        return f"Fejl i AI-analyse: {e}"
