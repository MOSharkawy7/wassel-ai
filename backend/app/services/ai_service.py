from app.models import Business, Customer, Conversation, Product


def generate_ai_response(
    business: Business,
    customer: Customer,
    conversation: Conversation,
    message: str,
    products: list[Product],
) -> str:
    """
    Generate a response using the business's real product data.

    This is still a temporary local AI engine.
    A real LLM will replace this logic later.
    """

    message_lower = message.lower()

    if "price" in message_lower or "سعر" in message_lower or "بكام" in message_lower:
        if not products:
            return (
                "أهلاً بيك 👋\n"
                "حالياً مش لاقي معلومات عن المنتجات والأسعار."
            )

        available_products = [
            product
            for product in products
            if product.is_available
        ]

        if not available_products:
            return (
                "أهلاً بيك 👋\n"
                "حالياً مفيش منتجات متاحة."
            )

        product_lines = []

        for product in available_products:
            product_lines.append(
                f"{product.name}: {product.price} {product.currency}"
            )

        return (
            "أهلاً بيك 👋\n"
            "المنتجات والأسعار المتاحة حالياً:\n\n"
            + "\n".join(product_lines)
        )

    if "hello" in message_lower or "hi" in message_lower:
        return (
            f"أهلاً بيك يا {customer.name or 'صديقي'} 👋\n"
            f"نورت {business.name}! إزاي أقدر أساعدك؟"
        )

    if "موجود" in message_lower or "available" in message_lower:
        available_products = [
            product
            for product in products
            if product.is_available
        ]

        if not available_products:
            return "حالياً مفيش منتجات متاحة."

        product_names = [
            product.name
            for product in available_products
        ]

        return (
            "أيوه طبعاً 👌\n"
            "المنتجات المتاحة حالياً:\n"
            + "\n".join(f"- {name}" for name in product_names)
        )

    return (
        "أهلاً بيك 👋\n"
        "أنا مساعد Wassel AI. ممكن تقولي محتاج إيه وأنا هساعدك."
    )