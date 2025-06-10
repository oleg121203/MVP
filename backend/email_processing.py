from typing import Dict, Any
from fastapi import APIRouter, UploadFile, File
from .email_classifier import EmailClassifier
from .response_templates import TemplateManager
import email
from email import policy
from email.parser import BytesParser

router = APIRouter()
classifier = EmailClassifier()
template_manager = TemplateManager()

@router.post("/email/process")
async def process_email(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Process an email file and extract key information.
    Returns structured JSON with email data and suggested response.
    """
    try:
        # Parse the email file
        email_content = await file.read()
        msg = BytesParser(policy=policy.default).parsebytes(email_content)
        body = msg.get_body(preferencelist=('plain', 'html')).get_content()
        
        # Classify the email
        classification = classifier.predict(body)
        
        # Get appropriate response template
        template = template_manager.get_template(classification["category"])
        suggested_response = None
        if template:
            email_data = {
                "from": msg["from"],
                "subject": msg["subject"],
                "date": msg["date"]
            }
            suggested_response = template_manager.generate_response(template.id, email_data)
        
        # Return complete email data
        return {
            "status": "success",
            "data": {
                "from": msg["from"],
                "to": msg["to"],
                "subject": msg["subject"],
                "date": msg["date"],
                "body": body,
                "classification": classification,
                "suggested_response": suggested_response
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
