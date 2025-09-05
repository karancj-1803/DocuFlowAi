# chatbot.py
from models import Document
from flask import jsonify
from sqlalchemy import desc
import re

def handle_chat_query(user_input, user_id):
    user_input = user_input.lower()

    if "last document" in user_input or "recent upload" in user_input:
        doc = Document.query.filter_by(user_id=user_id).order_by(desc(Document.uploaded_at)).first()
        if doc:
            return f"Your last uploaded document is '{doc.original_filename}' and its status is '{doc.status}'."
        else:
            return "You haven't uploaded any documents yet."

    elif "how many" in user_input:
        match = re.search(r"how many documents.*?(resume|invoice|contract|bank statement)", user_input)
        if match:
            doc_type = match.group(1).title()
            count = Document.query.filter_by(document_type=doc_type, user_id=user_id).count()
            return f"You have {count} documents classified as {doc_type}s."

    return "Sorry, I didn't understand that. Try asking about your recent uploads or document counts."
