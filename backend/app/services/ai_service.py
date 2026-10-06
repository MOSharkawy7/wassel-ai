from openai import OpenAI

from app.core.config import settings
from app.models import Business, Customer, Conversation, Product


client = OpenAI(
    api_key=settings.openai_api_key,
)


def generate_ai_response(
    business: Business,
    customer: Customer,
    conversation: Conversation,
    message: str,
    products: list[Product],
) -> str:
    product_context = []

    for product in products:
        availability = "Available" if product.is_available else "Unavailable"

        product_context.append(
            f"""
Product:
Name: {product.name}
Description: {product.description or "No description"}
Price: {product.price} {product.currency}
Availability: {availability}
""".strip()
        )

    products_text = "\n\n".join(product_context)

    system_prompt = f"""
You are Wassel AI, an AI customer service and sales assistant.

You work for:
Business name: {business.name}
Business description: {business.description or "No description"}
Business phone: {business.phone_number or "Not provided"}

Your job is to:
- Help customers professionally.
- Understand Egyptian Arabic, English, and mixed Arabic-English messages.
- Answer questions using the business information provided.
- Be friendly, concise, and natural.
- Help customers understand products and prices.
- Never invent product information, prices, availability, discounts,
  policies, or other business information.
- If the requested information is not available in the provided context,
  clearly tell the customer that you don't have that information.
- Never claim that you completed an action unless the system actually
  completed it.
- If the customer wants something that requires a human employee,
  politely indicate that a team member can assist them.

Customer:
Name: {customer.name or "Unknown"}
Phone: {customer.phone_number}

Business products:
{products_text or "No products have been added yet."}
""".strip()

    response = client.responses.create(
        model=settings.openai_model,
        instructions=system_prompt,
        input=message,
    )

    return response.output_text.strip()