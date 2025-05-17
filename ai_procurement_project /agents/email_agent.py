from config import llm
from utils.error import EmailDraftingError

def draft_email(to_email, product_details):
    try:
        prompt = f"""
        Draft a professional quotation request email with the following details:

        To: {to_email}
        Product: {product_details}

        Email Format:
        - Subject: Quotation Request for [Product Name]
        - Greeting: Always use "Dear Sir/Madam,"
        - Body: Mention interest in the product, specify quantity, ask for a quotation
        - Sign-off: "Regards,\nProcurement Manager\nXYZ"

        Ensure the tone is polite and professional. Avoid using placeholders like [Vendor's Name].
        """
        result = llm.invoke(prompt)
        return result.content
    except Exception as e:
        raise EmailDraftingError(f"Failed to draft email: {str(e)}")
