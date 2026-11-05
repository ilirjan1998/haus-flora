from django.core.management.base import BaseCommand
from booking.image_assets import prepare_variants
from booking.models import Photo


class Command(BaseCommand):
    help = "Create smaller WebP versions of active public property photos."

    def handle(self, *args, **options):
        count = prepare_variants(Photo.objects.filter(is_active=True))
        self.stdout.write(f"Prepared {count} responsive photo variants.")
