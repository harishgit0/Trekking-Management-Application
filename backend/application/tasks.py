from datetime import date
from application.models import User, Booking, Trek
from application.email_utils import send_email
from celery_worker import celery
import os
import csv
from datetime import datetime
from datetime import timedelta
from sqlalchemy import func
from application.database import db

@celery.task
def daily_reminder_task():
    """
    Send reminder emails to trekkers whose trek starts tomorrow.
    """

    tomorrow = date.today() + timedelta(days=1)

    bookings = (
        Booking.query.join(Trek)
        .filter(
            Trek.start_date == tomorrow,
            Booking.booking_status == "Booked"
        )
        .all()
    )

    reminders_sent = 0

    for booking in bookings:

        user = booking.user
        trek = booking.trek

        subject = f"Reminder: {trek.trek_name} starts tomorrow"

        body = f"""
Hello {user.username},

This is a reminder that your booked trek starts tomorrow.

Trek Details
-------------------------
Trek Name : {trek.trek_name}
Location  : {trek.location}
Difficulty: {trek.difficulty}
Start Date: {trek.start_date}
End Date  : {trek.end_date}

Please report at the meeting point at least 30 minutes before departure.

Carry the following:

• Government ID
• Trekking Shoes
• Water Bottle
• Rain Jacket
• Personal Medicines

Have a safe and enjoyable trek!

Regards,
Trekking Management Team
"""

        try:
            send_email(
                subject=subject,
                recipients=[user.email],
                body=body,
            )

            reminders_sent += 1
            print(f"Reminder sent to {user.email}")

        except Exception as e:
            print(f"Failed to send reminder to {user.email}: {e}")

    print(f"Daily Reminder Completed. Emails Sent: {reminders_sent}")

    return {
        "status": "success",
        "emails_sent": reminders_sent,
    }
# -----------------------------------------------------------------------------
# Monthly Report Task
# -----------------------------------------------------------------------------

@celery.task
def monthly_report_task():
    """
    Generate Monthly Activity Report for Admin
    and send it via HTML email.
    """

    admin = User.query.filter_by(role="admin").first()

    if not admin:
        print("Admin not found.")
        return "Admin not found"

    # ----------------------------------------------------
    # Statistics
    # ----------------------------------------------------

    total_bookings = Booking.query.count()

    completed_treks = Trek.query.filter_by(
        status="Completed"
    ).count()

    open_treks = Trek.query.filter_by(
        status="Open"
    ).count()

    pending_treks = Trek.query.filter_by(
        status="Pending"
    ).count()

    users_participated = (
        db.session.query(
            func.count(func.distinct(Booking.user_id))
        )
        .filter(
            Booking.booking_status == "Completed"
        )
        .scalar()
    )

    popular = (
        db.session.query(
            Trek.trek_name,
            func.count(Booking.id).label("total")
        )
        .join(Booking)
        .group_by(Trek.id)
        .order_by(func.count(Booking.id).desc())
        .first()
    )

    popular_trek = popular.trek_name if popular else "N/A"

    # ----------------------------------------------------
    # HTML Report
    # ----------------------------------------------------

    html = f"""
    <!DOCTYPE html>
    <html>

    <head>
        <meta charset="UTF-8">
    </head>

    <body style="font-family:Arial;background:#f4f4f4;padding:30px;">

        <div style="
            max-width:700px;
            margin:auto;
            background:white;
            border-radius:10px;
            padding:30px;
            box-shadow:0px 0px 10px rgba(0,0,0,0.1);
        ">

            <h2 style="text-align:center;color:#2E8B57;">
                🥾 Trekking Management System
            </h2>

            <h3 style="text-align:center;">
                Monthly Activity Report
            </h3>

            <p>Hello Admin,</p>

            <p>
                Here is your monthly trekking activity summary.
            </p>

            <table
                style="
                    width:100%;
                    border-collapse:collapse;
                    margin-top:20px;
                "
            >

                <tr style="background:#2E8B57;color:white;">
                    <th style="padding:10px;border:1px solid #ddd;">
                        Metric
                    </th>

                    <th style="padding:10px;border:1px solid #ddd;">
                        Value
                    </th>
                </tr>

                <tr>
                    <td style="padding:10px;border:1px solid #ddd;">
                        Total Bookings
                    </td>

                    <td style="padding:10px;border:1px solid #ddd;">
                        {total_bookings}
                    </td>
                </tr>

                <tr>
                    <td style="padding:10px;border:1px solid #ddd;">
                        Completed Treks
                    </td>

                    <td style="padding:10px;border:1px solid #ddd;">
                        {completed_treks}
                    </td>
                </tr>

                <tr>
                    <td style="padding:10px;border:1px solid #ddd;">
                        Open Treks
                    </td>

                    <td style="padding:10px;border:1px solid #ddd;">
                        {open_treks}
                    </td>
                </tr>

                <tr>
                    <td style="padding:10px;border:1px solid #ddd;">
                        Pending Treks
                    </td>

                    <td style="padding:10px;border:1px solid #ddd;">
                        {pending_treks}
                    </td>
                </tr>

                <tr>
                    <td style="padding:10px;border:1px solid #ddd;">
                        Users Participated
                    </td>

                    <td style="padding:10px;border:1px solid #ddd;">
                        {users_participated}
                    </td>
                </tr>

                <tr>
                    <td style="padding:10px;border:1px solid #ddd;">
                        Most Popular Trek
                    </td>

                    <td style="padding:10px;border:1px solid #ddd;">
                        {popular_trek}
                    </td>
                </tr>

            </table>

            <br>

            <h4>Summary</h4>

            <ul>
                <li>Total Bookings : <b>{total_bookings}</b></li>
                <li>Completed Treks : <b>{completed_treks}</b></li>
                <li>Open Treks : <b>{open_treks}</b></li>
                <li>Pending Treks : <b>{pending_treks}</b></li>
                <li>Users Participated : <b>{users_participated}</b></li>
                <li>Most Popular Trek : <b>{popular_trek}</b></li>
            </ul>

            <hr>

            <p style="font-size:14px;color:gray;">
                This report was automatically generated by the
                <strong>Trekking Management System</strong>.
            </p>

            <p>
                Regards,<br>
                Trekking Management Team
            </p>

        </div>

    </body>

    </html>
    """

    # ----------------------------------------------------
    # Send Email
    # ----------------------------------------------------

    try:

        send_email(
            subject="Monthly Trekking Activity Report",
            recipients=[admin.email],
            html=html,
        )

        print("Monthly report sent successfully.")

        return {
            "status": "success",
            "message": "Monthly report sent successfully.",
        }

    except Exception as e:

        print(f"Error sending monthly report: {e}")

        return {
            "status": "failed",
            "message": str(e),
        }
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