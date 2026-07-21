"""
Lotus Design - Full Stack Website
Flask + SQLite backend, HTML/CSS frontend
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import urllib.parse

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'lotus_design.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY', 'lotus-design-secret-key-change-this')

db = SQLAlchemy(app)

# ---------------- CONFIG (business info) ----------------
BUSINESS = {
    "name": "Lotus Design",
    "address": "Mainpur, Jamalpur, Bangladesh",
    "whatsapp": "+8801729335788",
    "whatsapp_link_number": "8801729335788",  # no + for wa.me links
    "phone": "+8801729335788",
    "email": "riazlotus01729335788@gmail.com",
}

# Admin login (change this password before going live!)
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'lotus123')

# ---------------- SERVICES ----------------
SERVICES = [
    {
        "id": "logo",
        "name": "Logo Design",
        "icon": "🎨",
        "price": "Starting at ৳800",
        "description": "Unique, memorable logo design that represents your brand identity.",
    },
    {
        "id": "business-card",
        "name": "Business Card Design",
        "icon": "💳",
        "price": "Starting at ৳500",
        "description": "Professional business card designs, print-ready in your preferred size.",
    },
    {
        "id": "banner",
        "name": "Banner Design",
        "icon": "🖼️",
        "price": "Starting at ৳600",
        "description": "Eye-catching banners for shops, events, and online ads.",
    },
    {
        "id": "poster",
        "name": "Poster Design",
        "icon": "📌",
        "price": "Starting at ৳700",
        "description": "Creative posters for promotions, events, and announcements.",
    },
    {
        "id": "social-media",
        "name": "Social Media Design",
        "icon": "📱",
        "price": "Starting at ৳400",
        "description": "Scroll-stopping post & story designs for Facebook, Instagram & more.",
    },
]

# ---------------- MODELS ----------------
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120))
    service = db.Column(db.String(80), nullable=False)
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default="New")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "service": self.service,
            "message": self.message,
            "status": self.status,
            "created_at": self.created_at.strftime("%d %b %Y, %I:%M %p"),
        }


# ---------------- PUBLIC ROUTES ----------------
@app.route('/')
def index():
    return render_template('index.html', business=BUSINESS, services=SERVICES)


@app.route('/order', methods=['POST'])
def place_order():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    email = request.form.get('email', '').strip()
    service = request.form.get('service', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not phone or not service:
        flash("Please fill in your name, phone number, and select a service.", "error")
        return redirect(url_for('index') + '#contact')

    order = Order(name=name, phone=phone, email=email, service=service, message=message)
    db.session.add(order)
    db.session.commit()

    # Build a WhatsApp message so the user can send it directly to Lotus Design
    wa_text = (
        f"Hello Lotus Design!\n"
        f"Name: {name}\n"
        f"Phone: {phone}\n"
        f"Service: {service}\n"
        f"Message: {message if message else '-'}"
    )
    wa_url = f"https://wa.me/{BUSINESS['whatsapp_link_number']}?text={urllib.parse.quote(wa_text)}"

    flash("Your order request has been received!", "success")
    return redirect(wa_url)


# ---------------- ADMIN ROUTES ----------------
def is_logged_in():
    return session.get('admin_logged_in', False)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        flash("Invalid username or password.", "error")
    return render_template('admin_login.html', business=BUSINESS)


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))


@app.route('/admin')
def admin_dashboard():
    if not is_logged_in():
        return redirect(url_for('admin_login'))
    orders = Order.query.order_by(Order.created_at.desc()).all()
    total = len(orders)
    new_count = len([o for o in orders if o.status == "New"])
    return render_template('admin.html', business=BUSINESS, orders=orders,
                            total=total, new_count=new_count)


@app.route('/admin/order/<int:order_id>/status', methods=['POST'])
def update_order_status(order_id):
    if not is_logged_in():
        return redirect(url_for('admin_login'))
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    if new_status in ("New", "In Progress", "Completed"):
        order.status = new_status
        db.session.commit()
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/order/<int:order_id>/delete', methods=['POST'])
def delete_order(order_id):
    if not is_logged_in():
        return redirect(url_for('admin_login'))
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


# ---------------- MAIN ----------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
