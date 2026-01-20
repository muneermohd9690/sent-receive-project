from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import CartItem


# We don't import the other models at the top to prevent circular errors
@receiver(post_save)
def sync_dispatch_date_to_cart(sender, instance, **kwargs):
    # Check if the sender is one of the models we care about
    if sender.__name__ in ['ItemDetails', 'TonerDetails']:

        # Only sync if there is a dispatch date
        if hasattr(instance, 'date_dispatched') and instance.date_dispatched:
            content_type = ContentType.objects.get_for_model(instance)

            # Find the CartItem that points to this specific Hardware/Toner
            # and sync the date and dispatched status
            CartItem.objects.filter(
                content_type=content_type,
                object_id=instance.id
            ).update(
                date_dispatched=instance.date_dispatched,
                dispatched=True
            )