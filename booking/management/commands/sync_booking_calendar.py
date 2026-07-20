from django.core.management.base import BaseCommand, CommandError

from booking.ical_sync import sync_booking_calendar


class Command(BaseCommand):
    help = "Synchronisiert den Booking.com-iCal-Kalender sofort."

    def handle(self, *args, **options):
        try:
            result = sync_booking_calendar(force=True)
        except Exception as exc:
            raise CommandError(str(exc)) from exc

        if result["status"] == "disabled":
            self.stdout.write(self.style.WARNING(
                "Booking.com-Synchronisation ist im Admin deaktiviert."
            ))
            return
        self.stdout.write(self.style.SUCCESS(
            f"Booking.com erfolgreich synchronisiert: {result['imported']} Zeitraum/Zeiträume."
        ))
