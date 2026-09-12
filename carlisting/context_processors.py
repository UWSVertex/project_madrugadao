import json

from django.conf import settings


def whatsapp(request):
    """Expose the rotating WhatsApp sales numbers to every template."""
    numbers = getattr(settings, 'WHATSAPP_NUMBERS', [])
    return {
        'WHATSAPP_NUMBERS': numbers,
        'WHATSAPP_NUMBERS_JSON': json.dumps(numbers),
    }
