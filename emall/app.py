import os
import time
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import bcrypt
from Crypto.Cipher import AES
import base64
from flask_session import Session
import redis

from emall.database import Database
from emall.config import config

def create_app():
    app = Flask(__name__)
    config_name = os.getenv('FLASK_ENV', 'development')
    if config_name == 'development' and os.getenv('DOCKER'):
        config_name = 'development_docker'
    app.config.from_object(config[config_name])
    print(f'CURRENT_ENV: {config_name}')

    app.config['IMAGE_FOLDER'] = './static/img'
    app.secret_key = 'sysu_software_engineer_project'  # 用于Flask应用的安全功能，例如会话（session）和CSRF保护
    encryption_key = b'2130702421307024'  # 用于AES加密和解密操作的密钥

    # 配置 Redis 作为会话存储
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_KEY_PREFIX'] = 'session:'
    app.config['SESSION_REDIS'] = redis.StrictRedis(host='redis', port=6379)
    Session(app)

    db = Database(host=app.config['DB_HOST'])

    def decrypt_password(encrypted_password):
        cipher = AES.new(encryption_key, AES.MODE_ECB)
        decoded = base64.b64decode(encrypted_password)
        decrypted_password = cipher.decrypt(decoded).decode('utf-8').rstrip('\x00')
        return decrypted_password


    @app.route('/logout')
    def logout():
        if 'username' in session:
            session.pop('username')
        return redirect(url_for('login'))


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """
        登录界面
        """
        if request.method == 'POST':
            username = request.form.get('username')
            # password = request.form.get('password')
            encrypted_password = request.form.get('password')
            print(encrypted_password)
            password = decrypt_password(encrypted_password).encode('utf-8')

            hashed_password = db.get_users_password(username)
            
            if hashed_password and bcrypt.checkpw(password, hashed_password.encode('utf-8')):
                session['username'] = username
                return redirect(url_for('index'))
            else:
                hashed_password_ad = db.get_admins_password(username)
                print(hashed_password_ad)
                if hashed_password_ad and bcrypt.checkpw(password, hashed_password_ad.encode('utf-8')):
                    session['adminname'] = username
                    return redirect(url_for('admin_index'))
                else:
                    flash('Invalid username or password', 'error')
                
            if db.user_login(username, password):
                session['username'] = username
                return redirect(url_for('index'))
            elif db.admin_login(username, password):
                session['adminname'] = username
                return redirect(url_for('admin_index'))
            else:
                flash('Invalid username or password', 'error')

        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """
        注册界面
        """
        if request.method == 'POST':
            username = request.form.get('username')
            # password = request.form.get('password')
            encrypted_password = request.form.get('password')
            print(encrypted_password)
            password = decrypt_password(encrypted_password).encode('utf-8')
            email = request.form.get('email')
            sex = request.form.get('sex')
            birthday = request.form.get('birthday')
            address = request.form.get('address')
            phone = request.form.get('phone')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
            info = {
                'username': username,
                'password': hashed_password,
                'email': email,
                'sex': sex,
                'birthday': birthday,
                'address': address,
                'phone': phone
            }
            print(info)
            if db.register(info):
                session['username'] = username
                # session['password'] = password
                session['password'] = hashed_password
                print("注册成功")
                return redirect(url_for('index'))
            else:
                flash('Invalid info for registeration', 'error')
        
        return render_template('register.html')

    @app.route('/cart', methods=['GET', 'POST'])
    def cart():
        """
        购物车
        """
        if request.method == 'GET':
            if 'username' in session.keys():
                username = session['username']
                cart_items, cart_total_price = db.show_cart(username)
                return render_template('shopping_cart.html', cart_items=cart_items, 
                                    cart_total_price=cart_total_price, username=username)
            else:
                return redirect(url_for('login'))
            
        username = session['username']
        cart_items, cart_total_price = db.show_cart(username)
        if len(cart_items) == 0:
            return redirect(url_for('cart'))
        db.make_order(username)
        return redirect(url_for('index'))


    @app.route('/add_to_cart', methods=['POST'])
    def add_to_cart():
        """
        将商品加入购物车
        """
        goods_name = request.form.get('goods_name')
        username = session['username']
        db.add_to_cart(username, goods_name)
        return redirect(url_for('index'))


    @app.route('/detail')
    def show_orders():
        """
        展示用户订单信息
        """
        if 'username' in session.keys():
            username = session['username']
            order_items = db.get_all_orders_for_user(username)
            return render_template('detail.html', order_data=order_items, username=username)
        else:
            return redirect(url_for('login'))


    @app.route('/', methods=['GET', 'POST'])
    def index():
        """
        首页
        """
        if 'username' in session.keys():
            username = session['username']
            cart_quantity = db.get_goods_quantity_in_cart(username)
        else:
            username = '请登录'
            cart_quantity = 0

        if request.method == 'GET':
            goods_items = db.get_all_goods()
            return render_template('index.html', goods_data=goods_items, username=username, cart_quantity=cart_quantity)
        
        name = request.form.get('search_query')
        goods_items = db.search_goods(name)
        return render_template('index.html', goods_data=goods_items, username=username, cart_quantity=cart_quantity)


    @app.route('/admin', methods=['GET', 'POST'])
    def admin_index():
        """
        管理员首页
        """
        if 'adminname' not in session.keys():
            return redirect(url_for('login'))
        
        adminname = session['adminname']
        goods_item = db.get_all_goods_for_admin()
        goods_quantity = db.get_goods_quantity_for_admin()

        if request.method == 'POST':
            update_items = []
            length = int(request.form.get('total_rows'))
            for i in range(length):
                item = {
                    'goods_name': request.form.get(f'goods_data[{i}][goods_name]'),
                    'type': request.form.get(f'goods_data[{i}][type]'),
                    'price': round(float(request.form.get(f'goods_data[{i}][price]')), 2),
                    'discount': round(float(request.form.get(f'goods_data[{i}][discount]')), 2),
                    'price_discount': round(float(request.form.get(f'goods_data[{i}][price_discount]')), 2),
                    'sales': int(request.form.get(f'goods_data[{i}][sales]'))
                }
                update_items.append(item)
            db.modify_goods_info_for_admin(update_items)
            goods_item = db.get_all_goods_for_admin()
            goods_quantity = db.get_goods_quantity_for_admin()

        return render_template('admin.html', goods_data=goods_item, goods_quantity=goods_quantity, username=adminname)

    @app.route('/admin/add_goods', methods=['PUT'])
    def add_goods():
        """
        增加新的商品信息
        """
        goods_name = request.form.get('product_name')
        typename = request.form.get('product_category')
        price = request.form.get('product_price')
        discount = request.form.get('product_discount')
        image = request.files['product_image']

        db.add_goods(goods_name, typename, price, discount)
        image.save(os.path.join(app.config['IMAGE_FOLDER'], f'{goods_name}.jpg'))
        return jsonify({'status': "success", 'message': "success"})


    @app.route('/admin/order')
    def show_all_orders():
        """
        管理员查看所有订单信息
        """
        if 'adminname' not in session.keys():
            return redirect(url_for('login'))
        
        adminname = session['adminname']
        order_data = db.get_all_orders_for_admin()

        return render_template('orders.html', order_data=order_data, username=adminname)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8082)