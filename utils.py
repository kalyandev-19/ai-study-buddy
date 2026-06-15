import io
import json
import PyPDF2
from google import genai
from google.genai import types

def extract_text_from_pdf(file_bytes):
    """Extracts text from a PDF file provided as bytes."""
    try:
        pdf_file = io.BytesIO(file_bytes)
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def get_client(api_key):
    """Creates and returns a google-genai client."""
    return genai.Client(api_key=api_key)

def explain_concept(api_key, topic, audience_level, style):
    """
    Explains a concept/topic using the new Gemini API.
    audience_level: 'Grade School (Explain Like I'm 5)', 'High School Student', 'College Student', 'Expert Practitioner'
    style: 'Simple & Direct', 'Analogy-rich (uses real-world comparisons)', 'Step-by-step Breakdown', 'Storytelling / Narrative format'
    """
    client = get_client(api_key)
    
    prompt = f"""
    You are an expert tutor. Please explain the following topic/concept:
    Topic: "{topic}"
    
    Target Audience Level: {audience_level}
    Explanation Style: {style}
    
    Provide a well-structured explanation. Use Markdown formatting to make it readable, engaging, and clear.
    Include:
    1. A simplified core definition.
    2. The key concepts explained in terms suitable for the audience and style.
    3. An illustrative example or analogy.
    4. A quick summary or "Takeaway".
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"API Error: {str(e)}"

def summarize_notes(api_key, notes_text):
    """
    Summarizes study notes. Returns a structured markdown summary.
    """
    client = get_client(api_key)
    
    prompt = f"""
    You are an expert student assistant. Please analyze the following study notes and create a structured summary:
    
    Study Notes:
    \"\"\"
    {notes_text}
    \"\"\"
    
    Format your response EXACTLY with these sections in Markdown:
    
    # Overview
    (A concise, clear 3-4 sentence paragraph summarizing the notes)
    
    # Key Takeaways
    * (Bullet points of the most important concepts, equations, facts, or theories)
    * (Add as many bullet points as necessary for thoroughness)
    
    # Glossary of Key Terms
    - **Term 1**: Brief and clear definition.
    - **Term 2**: Brief and clear definition.
    - ...
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"API Error: {str(e)}"

def generate_flashcards(api_key, topic_or_notes, num_cards=5):
    """
    Generates flashcards from a topic or notes using structured JSON.
    Returns a list of dicts: [{'front': '...', 'back': '...'}]
    """
    client = get_client(api_key)
    
    prompt = f"""
    Generate {num_cards} study flashcards based on the following topic or material:
    "{topic_or_notes}"
    
    Return the response as a JSON array of objects. Each object must represent a card and have exactly two string fields:
    - "front": The question or prompt (keep it concise, clear, and challenging)
    - "back": The answer or explanation (keep it clear, accurate, and bite-sized)
    
    Ensure the output is valid JSON and contains nothing else. Do not wrap in ```json or any markdown formatting.
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        return [{"front": "Error generating flashcards", "back": str(e)}]

def generate_quiz(api_key, topic_or_notes, num_questions=5):
    """
    Generates a multiple choice quiz from a topic or notes.
    Returns a list of dicts with question, options, answer, and explanation.
    """
    client = get_client(api_key)
    
    prompt = f"""
    Generate a multiple-choice quiz of {num_questions} questions based on the following topic or material:
    "{topic_or_notes}"
    
    Return the response as a JSON array of objects. Each object must have exactly four fields:
    - "question": The question text.
    - "options": An array of exactly 4 strings representing the multiple choice options.
    - "answer": An integer (0, 1, 2, or 3) representing the index of the correct option in the "options" array.
    - "explanation": A detailed explanation of why the correct option is right and others are wrong.
    
    Ensure the output is valid JSON and contains nothing else. Do not wrap in ```json or any markdown formatting.
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        return [{
            "question": "Error generating quiz",
            "options": ["Error", "Error", "Error", "Error"],
            "answer": 0,
            "explanation": str(e)
        }]

def ask_study_chat(api_key, history, new_message):
    """
    Sends a query to a conversational chat using the history.
    history is a list of {"role": "user"/"model", "content": "..."}
    """
    client = get_client(api_key)
    
    # Format the history for google-genai SDK
    formatted_history = []
    for msg in history:
        formatted_history.append(
            types.Content(
                role="user" if msg["role"] == "user" else "model",
                parts=[types.Part.from_text(text=msg["content"])]
            )
        )
        
    try:
        chat = client.chats.create(
            model="gemini-3.5-flash",
            history=formatted_history
        )
        response = chat.send_message(new_message)
        return response.text
    except Exception as e:
        return f"API Error: {str(e)}"
