from django.apps import AppConfig

class SentItemsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sent_items'

    def ready(self):
        # Using the full path ensures Django finds it correctly
        try:
            import sent_items.signals
        except ImportError as e:
            # This helps you see exactly why it's failing in the console
            print(f"Signal Import Error: {e}")
