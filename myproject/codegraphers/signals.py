from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Author, Book, AuthorProfile

@receiver(post_save, sender=Author)
def create_author_profile(sender, instance, created, **kwargs):
    if created:
        AuthorProfile.objects.create(author=instance)
        print(f"✅ Profile created for author: {instance.name}")

@receiver(post_save, sender=Book)
def update_author_stats_on_book_create(sender, instance, created, **kwargs):
    if created:
        profile = instance.author.profile
        profile.total_books = instance.author.books.count()
        profile.total_revenue += instance.price
        profile.save()
        print(f"📚 Updated {instance.author.name}'s stats: {profile.total_books} books, ${profile.total_revenue} revenue")

@receiver(post_delete, sender=Book)
def update_author_stats_on_book_delete(sender, instance, **kwargs):
    try:
        profile = instance.author.profile
        profile.total_books = instance.author.books.count()
        profile.total_revenue -= instance.price
        if profile.total_revenue < 0:
            profile.total_revenue = 0
        profile.save()
        print(f"🗑️ Book deleted. Updated {instance.author.name}'s stats")
    except Author.DoesNotExist:
        pass

@receiver(pre_save, sender=Book)
def validate_book_price(sender, instance, **kwargs):
    if instance.price < 0:
        instance.price = 0
        print(f"⚠️ Price adjusted to 0 for book: {instance.title}")
    
    if instance.price > 1000:
        print(f"💰 High-value book detected: {instance.title} at ${instance.price}")

@receiver(post_save, sender=Book)
def notify_book_unavailable(sender, instance, created, **kwargs):
    if not created and not instance.is_available:
        print(f"📧 Email sent: '{instance.title}' is now unavailable")