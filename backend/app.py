from flask import Flask, request, jsonify

from application import create_app
from application.database import db
from application.models import *
from application.cache import cache

from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt,
    get_jwt_identity,
)

from datetime import datetime, date

from application.tasks import (
    test_task,
    export_booking_history,
)

# -----------------------------------------------------------------------------
# App Initialization
# -----------------------------------------------------------------------------

app = create_app()

# -----------------------------------------------------------------------------
# Authentication APIs
# -----------------------------------------------------------------------------


@app.route("/trekker/export_bookings", methods=["POST"])
@jwt_required()
def export_bookings_api():

    claims = get_jwt()

    if claims["role"] != "trekker":
        return jsonify({"message": "Access denied"}), 403

    user_id = get_jwt_identity()

    task = export_booking_history.delay(user_id)

    return jsonify(
        {
            "message": "Export started",
            "task_id": task.id,
        }
    ), 202


@app.route("/register", methods=["POST"])
def register_api():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    full_name = data.get("full_name")
    phone = data.get("phone")
    age = data.get("age")
    gender = data.get("gender")
    address = data.get("address")

    if not username or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    if password != confirm_password:
        return jsonify({"message": "Passwords do not match"}), 400

    if not all([full_name, phone, age, gender, address]):
        return jsonify({"message": "All profile fields are required"}), 400

    hashed_password = generate_password_hash(password)

    user = User(
        username=username,
        email=email,
        password=hashed_password,
        role="trekker",
    )

    db.session.add(user)
    db.session.flush()

    profile = UserProfile(
        user_id=user.id,
        full_name=full_name,
        phone=phone,
        age=age,
        gender=gender,
        address=address,
    )

    db.session.add(profile)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login_api():

    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "All fields are required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid password"}), 401

    if not user.active_status:
        return jsonify({"message": "Your account has been blocked"}), 403

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role},
    )

    return jsonify(
        {
            "message": "Login successful",
            "token": access_token,
            "user": {
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
        }
    ), 200


@app.route("/logout", methods=["POST"])
@jwt_required()
def logout_api():
    return jsonify({"message": "Logout successful"}), 200


# -----------------------------------------------------------------------------
# Admin APIs
# -----------------------------------------------------------------------------
# -----------------------------------------------Admin APIs-----------------------------------------------------

# -----------------------------------------------------------------------------
# Trek Management APIs
# -----------------------------------------------------------------------------

@app.route("/admin/create_trek", methods=["POST"])
@jwt_required()
def create_trek_api():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"}), 400

    trek_name = data.get("trek_name")
    location = data.get("location")
    description = data.get("description")
    difficulty = data.get("difficulty")
    duration_days = int(data.get("duration_days"))
    total_slots = int(data.get("total_slots"))
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    if not all([
        trek_name,
        location,
        description,
        difficulty,
        duration_days,
        total_slots,
        start_date,
        end_date,
    ]):
        return jsonify({"message": "All fields are required"}), 400

    start_date = datetime.strptime(start_date, "%d-%m-%Y").date()
    end_date = datetime.strptime(end_date, "%d-%m-%Y").date()

    if start_date > end_date:
        return jsonify({
            "message": "Start date cannot be after end date"
        }), 400

    if duration_days <= 0:
        return jsonify({
            "message": "Duration must be greater than 0"
        }), 400

    if total_slots <= 0:
        return jsonify({
            "message": "Total slots must be greater than 0"
        }), 400

    trek = Trek(
        trek_name=trek_name,
        location=location,
        description=description,
        difficulty=difficulty,
        duration_days=duration_days,
        total_slots=total_slots,
        available_slots=total_slots,
        start_date=start_date,
        end_date=end_date,
    )

    db.session.add(trek)
    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Trek created successfully",
        "trek_id": trek.id,
    }), 201


@app.route("/admin/get_trek/<int:trek_id>", methods=["GET"])
@jwt_required()
def get_trek_api(trek_id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    return jsonify(trek.to_dict()), 200


@app.route("/admin/dashboard_counts", methods=["GET"])
@jwt_required()
@cache.cached(timeout=300)
def dashboard_counts_api():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    return jsonify({
        "trek_count": Trek.query.count(),
        "trekker_count": User.query.filter_by(role="trekker").count(),
        "staff_count": User.query.filter_by(role="staff").count(),
        "booking_count": Booking.query.count(),
    }), 200


@app.route("/admin/get_treks", methods=["GET"])
@jwt_required()
@cache.cached(timeout=300)
def get_treks_api():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    treks = Trek.query.all()

    return jsonify({
        "treks": [trek.to_dict() for trek in treks]
    }), 200


@app.route("/admin/delete_trek/<int:trek_id>", methods=["DELETE"])
@jwt_required()
def delete_trek_api(trek_id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    db.session.delete(trek)
    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Trek deleted successfully"
    }), 200


@app.route("/admin/update_trek/<int:trek_id>", methods=["PUT"])
@jwt_required()
def update_trek_api(trek_id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    data = request.get_json()

    trek.trek_name = data.get("trek_name")
    trek.location = data.get("location")
    trek.description = data.get("description")
    trek.difficulty = data.get("difficulty")
    trek.duration_days = data.get("duration_days")
    trek.total_slots = data.get("total_slots")
    trek.available_slots = data.get("available_slots")
    trek.status = data.get("status")

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Trek updated successfully"
    }), 200
# -----------------------------------------------------------------------------
# Trekker Management APIs
# -----------------------------------------------------------------------------

@app.route("/admin/trekkers", methods=["GET"])
@jwt_required()
@cache.cached(timeout=300)
def get_trekkers_api():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    trekkers = User.query.filter_by(role="trekker").all()

    return jsonify({
        "trekkers": [trekker.to_dict() for trekker in trekkers]
    }), 200


@app.route("/admin/get_trekker/<int:trekker_id>", methods=["GET"])
@jwt_required()
def get_trekker_api(trekker_id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    trekker = User.query.get(trekker_id)

    if not trekker:
        return jsonify({"message": "Trekker not found"}), 404

    return jsonify({
        "id": trekker.id,
        "username": trekker.username,
        "email": trekker.email,
        "active_status": trekker.active_status,
        "full_name": trekker.profile.full_name if trekker.profile else "",
        "phone": trekker.profile.phone if trekker.profile else "",
        "age": trekker.profile.age if trekker.profile else "",
        "gender": trekker.profile.gender if trekker.profile else "",
        "address": trekker.profile.address if trekker.profile else "",
    }), 200


@app.route("/admin/update_trekker/<int:trekker_id>", methods=["PUT"])
@jwt_required()
def update_trekker_api(trekker_id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    trekker = User.query.get(trekker_id)

    if not trekker:
        return jsonify({"message": "Trekker not found"}), 404

    data = request.get_json()

    trekker.username = data.get("username")
    trekker.email = data.get("email")
    trekker.active_status = data.get("active_status")

    if trekker.profile:
        trekker.profile.full_name = data.get("full_name")
        trekker.profile.phone = data.get("phone")
        trekker.profile.age = data.get("age")
        trekker.profile.gender = data.get("gender")
        trekker.profile.address = data.get("address")

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Trekker updated successfully"
    }), 200


@app.route("/admin/block_user/<int:user_id>", methods=["PUT"])
@jwt_required()
def block_user_api(user_id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    if user.role != "trekker":
        return jsonify({"message": "User is not trekker"}), 400

    user.active_status = False

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "User blocked successfully"
    }), 200


# -----------------------------------------------------------------------------
# Staff Management APIs
# -----------------------------------------------------------------------------

@app.route("/admin/staff", methods=["GET"])
@jwt_required()
@cache.cached(timeout=300)
def staff_api():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    staff_list = User.query.filter_by(role="staff").all()

    result = []

    for staff in staff_list:
        result.append({
            "id": staff.id,
            "username": staff.username,
            "email": staff.email,
            "active_status": staff.active_status,
            "full_name": staff.profile.full_name if staff.profile else "",
            "phone": staff.profile.phone if staff.profile else "",
            "assigned_treks": len(staff.staff_assignments)
        })

    return jsonify({"staff": result}), 200


@app.route("/admin/get_staff/<int:staff_id>", methods=["GET"])
@jwt_required()
def get_staff_api(staff_id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    staff = User.query.get(staff_id)

    if not staff:
        return jsonify({"message": "Staff not found"}), 404

    return jsonify({
        "id": staff.id,
        "username": staff.username,
        "email": staff.email,
        "active_status": staff.active_status,
        "full_name": staff.profile.full_name if staff.profile else "",
        "phone": staff.profile.phone if staff.profile else "",
        "age": staff.profile.age if staff.profile else "",
        "gender": staff.profile.gender if staff.profile else "",
        "address": staff.profile.address if staff.profile else "",
    }), 200


@app.route("/admin/update_staff/<int:staff_id>", methods=["PUT"])
@jwt_required()
def update_staff_api(staff_id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    staff = User.query.get(staff_id)

    if not staff:
        return jsonify({"message": "Staff not found"}), 404

    data = request.get_json()

    staff.username = data.get("username")
    staff.email = data.get("email")
    staff.active_status = data.get("active_status")

    if staff.profile:
        staff.profile.full_name = data.get("full_name")
        staff.profile.phone = data.get("phone")
        staff.profile.age = data.get("age")
        staff.profile.gender = data.get("gender")
        staff.profile.address = data.get("address")

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Staff updated successfully"
    }), 200
# -----------------------------------------------------------------------------
# Staff Creation & Assignment APIs
# -----------------------------------------------------------------------------

@app.route("/admin/add_staff", methods=["POST"])
@jwt_required()
def add_staff_api():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    full_name = data.get("full_name")
    phone = data.get("phone")
    age = data.get("age")
    gender = data.get("gender")
    address = data.get("address")

    if not username or not email or not password:
        return jsonify({
            "message": "Username, email and password are required"
        }), 400

    if User.query.filter_by(username=username).first():
        return jsonify({
            "message": "Username already exists"
        }), 400

    if User.query.filter_by(email=email).first():
        return jsonify({
            "message": "Email already exists"
        }), 400

    if not all([full_name, phone, age, gender, address]):
        return jsonify({
            "message": "All profile fields are required"
        }), 400

    hashed_password = generate_password_hash(password)

    staff = User(
        username=username,
        email=email,
        password=hashed_password,
        role="staff",
    )

    db.session.add(staff)
    db.session.flush()

    profile = UserProfile(
        user_id=staff.id,
        full_name=full_name,
        phone=phone,
        age=age,
        gender=gender,
        address=address,
    )

    db.session.add(profile)
    db.session.commit()

    cache.clear()

    return jsonify({
        "message": "Staff added successfully",
        "staff_id": staff.id,
        "staff_username": staff.username,
    }), 201


@app.route("/admin/block_staff/<int:staff_id>", methods=["PUT"])
@jwt_required()
def block_staff_api(staff_id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    staff = User.query.get(staff_id)

    if not staff:
        return jsonify({"message": "Staff not found"}), 404

    if staff.role != "staff":
        return jsonify({"message": "User is not staff"}), 400

    staff.active_status = False

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Staff blocked successfully"
    }), 200


@app.route("/admin/assign_staff", methods=["POST"])
@jwt_required()
def assign_staff_api():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"}), 400

    trek_id = data.get("trek_id")
    staff_id = data.get("staff_id")

    if not trek_id or not staff_id:
        return jsonify({
            "message": "trek_id and staff_id are required"
        }), 400

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    staff = User.query.get(staff_id)

    if not staff:
        return jsonify({"message": "Staff not found"}), 404

    if staff.role != "staff":
        return jsonify({"message": "User is not staff"}), 400

    if trek.status is False:
        return jsonify({
            "message": "Trek is inactive"
        }), 400

    existing_assignment = StaffAssignment.query.filter_by(
        trek_id=trek_id,
        staff_id=staff_id,
    ).first()

    if existing_assignment:
        return jsonify({
            "message": "Staff already assigned to this trek"
        }), 400

    trek_assignment = StaffAssignment.query.filter_by(
        trek_id=trek_id
    ).first()

    if trek_assignment:
        return jsonify({
            "message": "A staff member is already assigned to this trek"
        }), 400

    assignment = StaffAssignment(
        staff_id=staff_id,
        trek_id=trek_id,
        assigned_at=datetime.utcnow(),
    )

    db.session.add(assignment)
    db.session.commit()

    cache.clear()

    return jsonify({
        "message": "Staff assigned successfully"
    }), 201


@app.route("/admin/get_bookings", methods=["GET"])
@jwt_required()
@cache.cached(timeout=300)
def get_bookings_api():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    bookings = Booking.query.all()

    return jsonify({
        "bookings": [booking.to_dict() for booking in bookings]
    }), 200
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------Staff APIs----------------------------------------------------------



@app.route("/staff/dashboard_counts", methods=["GET"])
@jwt_required()
@cache.cached(timeout=300)
def staff_dashboard_counts_api():

    claim = get_jwt()
    staff_id = get_jwt_identity()

    if claim["role"] != "staff":
        return jsonify({"message": "Access denied"}), 403

    trek_count = StaffAssignment.query.filter_by(
        staff_id=staff_id
    ).count()
    assigned_treks=StaffAssignment.query.filter_by(
        staff_id=staff_id
    ).all()

    upcoming_count = StaffAssignment.query.join(Trek).filter(
        StaffAssignment.staff_id == staff_id,
        Trek.start_date > date.today()
    ).count()
    completed_count = StaffAssignment.query.join(Trek).filter(
        StaffAssignment.staff_id == staff_id,
        Trek.end_date < date.today()
    ).count()

    return jsonify({
        "total_assigned_treks": trek_count,
        "upcoming_treks": upcoming_count,
        "completed_treks": completed_count,
        "assigned_treks": [assigned_trek.to_dict() for assigned_trek in assigned_treks]
    }), 200



@app.route("/staff/get_treks", methods=["GET"])
@jwt_required()
@cache.cached(timeout=300)
def staff_get_treks_api():
    claim = get_jwt()
    staff_id = get_jwt_identity()

    if claim["role"] != "staff":
        return jsonify({"message": "Access denied"}), 403

    treks = Trek.query.join(StaffAssignment).filter(
        StaffAssignment.staff_id == staff_id
    ).all()

    return jsonify({"treks": [trek.to_dict() for trek in treks]}), 200

@app.route("/staff/update_trek/<int:trek_id>", methods=["PUT"])
@jwt_required()
def staff_update_trek_api(trek_id):

    claims = get_jwt()
    staff_id = get_jwt_identity()

    if claims["role"] != "staff":
        return jsonify({
            "message": "Access denied"
        }), 403

    assignment = StaffAssignment.query.filter_by(
        staff_id=staff_id,
        trek_id=trek_id
    ).first()

    if not assignment:
        return jsonify({
            "message": "You are not assigned to this trek"
        }), 403

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "message": "Trek not found"
        }), 404

    data = request.get_json()

    available_slots = data.get("available_slots")
    status = data.get("status")

    # Validate slots
    if available_slots is not None:

        if available_slots < 0:
            return jsonify({
                "message": "Available slots cannot be negative"
            }), 400

        if available_slots > trek.total_slots:
            return jsonify({
                "message": "Available slots cannot exceed total slots"
            }), 400

        trek.available_slots = available_slots

    # Validate status
    allowed_statuses = [
        "Pending",
        "Started",
        "Completed"
    ]

    if status is not None:

        if status not in allowed_statuses:
            return jsonify({
                "message": "Invalid status"
            }), 400

        trek.status = status

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Trek updated successfully",
        "trek": trek.to_dict()
    }), 200

@app.route("/staff/participants/<int:trek_id>", methods=["GET"])
@jwt_required()
def staff_get_participants_api(trek_id):

    claims = get_jwt()
    staff_id = get_jwt_identity()

    if claims["role"] != "staff":
        return jsonify({
            "message": "Access denied"
        }), 403

    # Check staff is assigned to this trek
    assignment = StaffAssignment.query.filter_by(
        staff_id=staff_id,
        trek_id=trek_id
    ).first()

    if not assignment:
        return jsonify({
            "message": "You are not assigned to this trek"
        }), 403

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "message": "Trek not found"
        }), 404

    participants = Booking.query.filter_by(
        trek_id=trek_id
    ).all()

    return jsonify({
        "trek": trek.to_dict(),
        "participants": [participant.to_dict() for participant in participants]
    }), 200

@app.route("/staff/profile", methods=["GET"])
@jwt_required()
def staff_profile_api():
    claims = get_jwt()
    staff_id = get_jwt_identity()

    if claims["role"] != "staff":
        return jsonify({
            "message": "Access denied"
        }), 403

    staff = User.query.get(staff_id)

    if not staff:
        return jsonify({
            "message": "Staff not found"
        }), 404

    return jsonify({
        "staff": staff.to_dict()
    }), 200

# --------------------------------------------------------------------------------------------------------------------



# --------------------------------------------------USER(TREKKER_APIs)-----------------------------



@app.route("/trekker/stats", methods=["GET"])
@jwt_required()
def trekker_stats_api():
    claims = get_jwt()
    

    if claims["role"] != "trekker":
        return jsonify({"message": "Access denied"}), 403

    user_id = get_jwt_identity()

    # Available treks
    available_treks = Trek.query.filter(
        Trek.available_slots > 0,
        Trek.start_date >= date.today(),
        Trek.status == "Approved"
    ).count()

    # Total bookings by this user
    booked_treks = Booking.query.filter_by(
        user_id=user_id
    ).count()

    # Upcoming booked treks
    upcoming_treks = Booking.query.join(Trek).filter(
        Booking.user_id == user_id,
        Trek.start_date > date.today()
    ).count()

    # Completed booked treks
    completed_treks = Booking.query.join(Trek).filter(
        Booking.user_id == user_id,
        Trek.end_date < date.today()
    ).count()

    return jsonify({
        "available_treks": available_treks,
        "booked_treks": booked_treks,
        "upcoming_treks": upcoming_treks,
        "completed_treks": completed_treks
    }), 200


@app.route("/trekker/treks", methods=["GET"])
@jwt_required()
@cache.cached(timeout=300)
def trekker_treks_api():
    claims = get_jwt()

    if claims["role"] != "trekker":
        return jsonify({"message": "Access denied"}), 403

    treks = Trek.query.filter(
        Trek.available_slots > 0,
        Trek.start_date >= date.today(),
        Trek.status == "Approved"
    ).all()

    return jsonify({
        "treks": [trek.to_dict() for trek in treks]
    }), 200


@app.route("/trekker/my_bookings", methods=["GET"])
@jwt_required()
def trekker_my_bookings_api():
    claims = get_jwt()

    if claims["role"] != "trekker":
        return jsonify({"message": "Access denied"}), 403

    user_id = get_jwt_identity()

    bookings = Booking.query.filter_by(
        user_id=user_id
    ).all()

    return jsonify({
        "bookings": [booking.to_dict() for booking in bookings]
    }), 200



@app.route("/trekker/book/<int:trek_id>", methods=["POST"])
@jwt_required()
def trekker_book_trek_api(trek_id):
    claims = get_jwt()

    if claims["role"] != "trekker":
        return jsonify({"message": "Access denied"}), 403

    user_id = get_jwt_identity()

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "message": "Trek not found"
        }), 404

    # Trek must be approved
    if trek.status != "Approved":
        return jsonify({
            "message": "This trek is not available for booking."
        }), 400

    # Slots available?
    if trek.available_slots <= 0:
        return jsonify({
            "message": "No slots available."
        }), 400

    # Prevent duplicate booking
    existing_booking = Booking.query.filter_by(
        user_id=user_id,
        trek_id=trek_id
    ).first()

    if existing_booking:
        return jsonify({
            "message": "You have already booked this trek."
        }), 400

    booking = Booking(
        user_id=user_id,
        trek_id=trek_id,
        booking_date=datetime.now(),
        booking_status="Booked"
    )

    # Reduce available slots
    trek.available_slots -= 1

    db.session.add(booking)
    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Trek booked successfully.",
        "booking": booking.to_dict()
    }), 201


@app.route("/trekker/history", methods=["GET"])
@jwt_required()
def trekker_history_api():
    claims = get_jwt()

    if claims["role"] != "trekker":
        return jsonify({"message": "Access denied"}), 403

    user_id = get_jwt_identity()

    bookings = Booking.query.join(Trek).filter(
        Booking.user_id == user_id,
        Trek.end_date < date.today()
    ).all()


    return jsonify({
        "history": [booking.to_dict() for booking in bookings]
    }), 200

@app.route("/trekker/profile", methods=["GET"])
@jwt_required()
def trekker_profile_api():
    claims = get_jwt()
    trekker_id = get_jwt_identity()

    if claims["role"] != "trekker":
        return jsonify({
            "message": "Access denied"
        }), 403

    trekker = User.query.get(trekker_id)

    if not trekker:
        return jsonify({
            "message": "Trekker not found"
        }), 404

    return jsonify({
        "trekker": trekker.to_dict()
    }), 200

# ---------------------------
# Initial Database Setup
# ---------------------------

with app.app_context():
    db.create_all()

    admin = User.query.filter_by(role="admin").first()

    if not admin:
        admin = User(
            username="admin",
            email="admin@trek.com",
            password=generate_password_hash("admin123"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()


# ---------------------------
# Testing Routes
# ---------------------------

@app.route("/test-cache")
@cache.cached(timeout=60)
def test_cache():
    print("🔥 TEST ROUTE EXECUTED")
    return jsonify({
        "message": "Cache is working!"
    })


@app.route("/test-celery")
def test_celery():
    task = test_task.delay()

    return jsonify({
        "message": "Task sent successfully!",
        "task_id": task.id
    })


# ---------------------------
# Run Application
# ---------------------------

if __name__ == "__main__":
    app.run(debug=True)