from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'

db = SQLAlchemy(app)

# 1. نموذج قائمة الطعام
class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(300), nullable=False)
    category = db.Column(db.String(50), nullable=False)

# 2. نموذج طلبات الدليفري والأوردرات
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    item_name = db.Column(db.String(100), nullable=False)

# 3. نموذج حجز الطاولات
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)

# لوحة التحكم
admin = Admin(app, name='لوحة تحكم المطعم')
admin.add_view(ModelView(MenuItem, db, name='إدارة المنيو'))
admin.add_view(ModelView(Order, db, name='طلبات الدليفري'))
admin.add_view(ModelView(Reservation, db, name='الحجوزات'))

@app.route('/')
def home():
    items = MenuItem.query.all()
    return render_template('index.html', items=items)

@app.route('/order', methods=['POST'])
def order():
    name = request.form.get('name')
    phone = request.form.get('phone')
    address = request.form.get('address')
    item_name = request.form.get('item_name')
    
    new_order = Order(customer_name=name, phone=phone, address=address, item_name=item_name)
    db.session.add(new_order)
    db.session.commit()
    
    flash('تم تسجيل طلب الدليفري بنجاح! سيتصل بك المندوب قريباً.')
    return redirect(url_for('home'))

@app.route('/reserve', methods=['POST'])
def reserve():
    name = request.form.get('name')
    phone = request.form.get('phone')
    date = request.form.get('date')
    time = request.form.get('time')
    
    new_res = Reservation(name=name, phone=phone, date=date, time=time)
    db.session.add(new_res)
    db.session.commit()
    
    flash('تم استلام طلب حجز الطاولة بنجاح!')
    return redirect(url_for('home'))

def seed_initial_data():
    if MenuItem.query.count() == 0:
        sample_items = [
            MenuItem(name="برجر كلاسيك فاخر", price=120.0, image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500", category="وجبات سريعة"),
            MenuItem(name="بيتزا بيتزا مارجريتا", price=150.0, image_url="https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500", category="بيتزا"),
            MenuItem(name="باستا إيطالي بالصوص الأبيض", price=110.0, image_url="https://images.unsplash.com/photo-1645112411341-6c4fd023714a?w=500", category="باستا"),
            MenuItem(name="وجبة مشويات مشكلة", price=250.0, image_url="https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=500", category="مشويات")
        ]
        db.session.bulk_save_objects(sample_items)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_initial_data()
    app.run(debug=True)