#### routes.py

from flask import Blueprint, jsonify, request
from models import Customer, Visit
from database import db
from datetime import datetime, timezone, timedelta


api = Blueprint("api", __name__)

@api.route("/api/health")
def health_check():
    return jsonify({
        "status": "running",
        "message": "ClipTracker API alive"
    })

@api.route("/api/customers", methods=["POST"])
def add_customer():
    
    data = request.json
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    phone_no = data.get("phone_no")

    if not first_name:
        return jsonify({"error": "First name required"}), 400
    
    try:
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            phone_no=phone_no,
            visit_count=0,
            cycle_start_date=datetime.now(timezone.utc)
        )

        db.session.add(customer)
        db.session.commit()

        return jsonify({
            "message": "Customer added",
            "customer_id": customer.id
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500
    
@api.route("/api/customers", methods=["GET"])
def get_customer():

    customers = Customer.query.all()

    results = []

    for c in customers:
        results.append({
            
            "id": c.id,
            "first_name": c.first_name,
            "last_name": c.last_name,
            "phone_no": c.phone_no,
            "visit_count": c.visit_count

        })

    return jsonify(results)

@api.route("/api/customers/<int:id>/visit", methods=["POST"])
def log_visits(id):
    try:
        customer = Customer.query.get(id)
        if not customer:
            return jsonify({"error": "Customer not found"}), 404
        

        now = datetime.utcnow()
        
        # ===== Fix for offset-naive vs aware =====
        cycle_start = customer.cycle_start_date
        if cycle_start:
            # Make sure cycle_start is naive UTC
            if cycle_start.tzinfo is not None:
                cycle_start = cycle_start.replace(tzinfo=None)

            # check if 6 months have passed since cycle start
            if (now - cycle_start) > timedelta(days=182):
                customer.visit_count = 0
                customer.cycle_start_date = now

        # increase visit count
        customer.visit_count += 1
        customer.last_visit_date = now

        # determine discount
        discount = "none"
        if customer.visit_count == 5:
            discount = "half_off"
        elif customer.visit_count == 10:
            discount = "free"
            customer.visit_count = 0 # reset cycle
            customer.cycle_start_date = now


        # create visit entry
        visit = Visit(
            customer_id=customer.id,
            visited_at=now,
            discount_applied=discount
        )

        db.session.add(visit)
        db.session.commit()

        return jsonify({
            "message": "Visit logged",
            "visit_id": visit.id,
            "discount": discount,
            "current_visit_count": customer.visit_count
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    




@api.route("/api/customers/<int:id>", methods=["GET"])
def fetch_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    visits = Visit.query.filter_by(customer_id=customer.id).order_by(Visit.visited_at.desc()).all()

    visits_history = []
    for v in visits:
        visits_history.append({
            "id": v.id,
            "visited_at": v.visited_at.isoformat(),
            "discount_applied": v.discount_applied,
            "notes": v.notes
        })

    return jsonify({
        "id": customer.id,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "phone_no": customer.phone_no,
        "visit_count": customer.visit_count,
        "cycle_start_date": customer.cycle_start_date.isoformat() if customer.cycle_start_date else None,
        "last_visit_date": customer.last_visit_date.isoformat() if customer.last_visit_date else None,
        "visit_history": visits_history
    })