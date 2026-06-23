from .database import db

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    active_status = db.Column(db.Boolean, nullable=False, default=True)

    profile = db.relationship("UserProfile",backref="user",uselist=False)

    bookings = db.relationship("Booking",backref="user")

    staff_assignments = db.relationship("StaffAssignment",backref="staff",foreign_keys="StaffAssignment.staff_id")


class UserProfile(db.Model):
    __tablename__ = "user_profile"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False,unique=True)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)


class Trek(db.Model):
    __tablename__ = "trek"

    id = db.Column(db.Integer, primary_key=True)
    trek_name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(120), nullable=False)

    duration_days = db.Column(db.Integer, nullable=False)
    total_slots = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)

    status = db.Column(db.String(120),nullable=False,default="Pending")

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    bookings = db.relationship("Booking",backref="trek")

    staff_assignments = db.relationship("StaffAssignment",backref="trek")


class Booking(db.Model):
    __tablename__ = "booking"
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trek_id=db.Column(db.Integer, db.ForeignKey('trek.id'), nullable=False)
    booking_date=db.Column(db.DateTime, nullable=False)
    booking_status=db.Column(db.String(120), nullable=False, default="Booked")

    __table_args__ = (
    db.UniqueConstraint(
        'user_id',
        'trek_id',
        name='unique_user_trek_booking'
    ),
)


class StaffAssignment(db.Model):
    __tablename__ = "staff_assignment"
    id=db.Column(db.Integer, primary_key=True)
    staff_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trek_id=db.Column(db.Integer, db.ForeignKey('trek.id'), nullable=False)
    assigned_at=db.Column(db.DateTime, nullable=False)

    __table_args__ = (
    db.UniqueConstraint(
        'staff_id',
        'trek_id',
        name='unique_staff_trek_assignment'
    ),
)