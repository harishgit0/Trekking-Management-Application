import csv
import os
from datetime import datetime

from celery_worker import celery
from application.models import Booking


# -----------------------------------------------------------------------------
# Test Task
# -----------------------------------------------------------------------------

@celery.task
def test_task():
    print("Celery working!")
    return "OK"


# -----------------------------------------------------------------------------
# Daily Reminder Task
# -----------------------------------------------------------------------------

@celery.task
def daily_reminder_task():
    print("Sending daily reminders...")
    return "Daily reminders sent"


# -----------------------------------------------------------------------------
# Monthly Report Task
# -----------------------------------------------------------------------------

@celery.task
def monthly_report_task():
    print("Generating monthly report...")
    return "Monthly report generated"


# -----------------------------------------------------------------------------
# Export Booking History
# -----------------------------------------------------------------------------

@celery.task
def export_booking_history(user_id):
    """
    Export all bookings of a trekker into a CSV file.
    """

    bookings = Booking.query.filter_by(user_id=user_id).all()

    os.makedirs("exports", exist_ok=True)

    filename = (
        f"booking_history_{user_id}_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

    filepath = os.path.join("exports", filename)

    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "User ID",
            "Trek Name",
            "Location",
            "Booking Status",
            "Booking Date",
        ])

        for booking in bookings:
            writer.writerow([
                booking.user_id,
                booking.trek.trek_name,
                booking.trek.location,
                booking.booking_status,
                booking.booking_date,
            ])

    print(f"Booking history exported to {filepath}")

    return filepath