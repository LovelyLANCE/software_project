import psycopg2
from psycopg2 import sql
from datetime import datetime
import os

class Database:
    def __init__(self, host='localhost'):

        dbname = 'mydatabase'
        if os.getenv('FLASK_ENV') == 'testing':
            dbname = 'test_mydatabase'
        elif os.getenv('FLASK_ENV') == 'production':
            dbname = 'prod_mydatabase'
        self.db_config = {
            'dbname': dbname,
            'user': 'postgres',
            'password': '123456',
            'host': host,
            'port': 5432
        }

    def get_users_password(self, username):
        """
        获取数据库中的已被hash的密码,客户
        """
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT password FROM users WHERE username = %s", (username,))
                    result = cur.fetchone()
                    if result:
                        return result[0]
                    else:
                        return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def get_admins_password(self, username):
        """
        获取数据库中的已被hash的密码,管理员
        """
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT password FROM admins WHERE username = %s", (username,))
                    result = cur.fetchone()
                    if result:
                        return result[0]
                    else:
                        return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def user_login(self, username, password):
        """
        用户登录检测函数
        """
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                # 准备 SQL 查询语句
                    query = sql.SQL("SELECT password FROM users WHERE username = %s;")
                    cur.execute(query, (username,))

                    # 获取查询结果
                    result = cur.fetchone()
                    if result and result[0] == password:
                        print(result[0])
                        return True
                    else:
                        print("Invalid username or password")
                        return False                    

        except psycopg2.Error as e:
            print("An error occurred:", e)
            if conn is not None:
                conn.close()
            return False
        
    def admin_login(self, username, password):
        """
        管理员登录检测函数
        """
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                # 准备 SQL 查询语句
                    query = sql.SQL("SELECT password FROM admins WHERE username = %s;")
                    cur.execute(query, (username,))

                    # 获取查询结果
                    result = cur.fetchone()
                    if result and result[0] == password:
                        print(result[0])
                        return True
                    else:
                        print("Invalid username or password")
                        return False                    

        except psycopg2.Error as e:
            print("An error occurred:", e)
            if conn is not None:
                conn.close()
            return False
    
    def register(self, info):
        """
        注册新用户，数据插入至数据库
        """
        username = info['username']
        password = info['password']
        email = info['email']
        sex = info['sex']
        birthday = info['birthday']
        address = info['address']
        phone = info['phone']

        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                        # SQL 插入语句
                        query = sql.SQL("""
                            INSERT INTO users (username, password, sex, birthday, address, phone, email) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s);
                        """)
                        
                        # 执行插入操作
                        cur.execute(query, (username, password, sex, birthday, address, phone, email))
                        
                        # 提交事务
                        conn.commit()
        except psycopg2.Error as e:
            print("An error occurred:", e)
            if conn is not None:
                conn.close()
            return False

        return True


    def register_admin(self, info):
        """
        注册新admin用户，数据插入至数据库
        """
        username = info['username']
        password = info['password']
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""
                        INSERT INTO admins (username, password)
                        VALUES (%s, %s);
                    """)
                    cur.execute(query, (username, password))
                    conn.commit()
        except psycopg2.Error as e:
            print("An error occurred:", e)
            if conn is not None:
                conn.close()
            return False

        return True
        
    
    def get_all_goods(self):
        """
        返回所有商品名和价格列表
        """
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    # 执行查询
                    cur.execute("SELECT goodsname, price, discount FROM goods;")
                    # 提取结果
                    goods_items = []
                    for record in cur.fetchall():
                        goods_name, price, discount = record
                        item = {'goods_name': goods_name, 'price': price, 'path': f'img/{goods_name}.jpg', 'price_discount': round(price*discount, 2)}
                        goods_items.append(item)

                    return goods_items

        except psycopg2.Error as e:
            print("An error occurred:", e)
            if conn is not None:
                conn.close()
            return [], []
    
    def get_goods_quantity_in_cart(self, username):
        """
        返回某个用户购物车商品数量
        """
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                     # 根据用户名查找user_id
                    cur.execute("SELECT user_id FROM users WHERE username = %s", (username,))
                    user_id = cur.fetchone()[0]

                    # 查询该用户购物车中所有商品的数量
                    cur.execute("SELECT SUM(quantity) FROM carts WHERE user_id = %s", (user_id,))
                    total_quantity = cur.fetchone()[0]

                    return total_quantity if total_quantity is not None else 0

        except psycopg2.Error as e:
            print("An error occurred:", e)
            if conn is not None:
                conn.close()
            return -1

    def search_goods(self, name):
        """
        返回指定的商品名和价格信息
        """
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    # 执行查询
                    cur.execute("SELECT goodsname, price, discount FROM goods WHERE goodsname ILIKE %s", (f'%{name}%',))
                    goods_items = []
                    for record in cur.fetchall():
                        goods_name, price, discount = record
                        item = {'goods_name': goods_name, 'price': price, 'path': f'img/{goods_name}.jpg', 'price_discount': round(price*discount, 2)}
                        goods_items.append(item)
                    return goods_items

        except psycopg2.Error as e:
            print("An error occurred:", e)
            if conn is not None:
                conn.close()
            return []
        
    def add_to_cart(self, username, goods_name):
        """
        将商品加入至购物车
        """
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT user_id FROM users WHERE username = %s;", (username,))
                    user_id = cur.fetchone()
                    user_id = user_id[0]
                    # 根据用户名查找user_id
                    cur.execute("SELECT user_id FROM users WHERE username = %s", (username,))
                    user_id = cur.fetchone()[0]

                    # 根据商品名查找goods_id
                    cur.execute("SELECT goods_id FROM goods WHERE goodsname = %s", (goods_name,))
                    goods_id = cur.fetchone()[0]

                    # 检查商品是否已在购物车中
                    cur.execute("SELECT quantity FROM carts WHERE user_id = %s AND goods_id = %s", (user_id, goods_id))
                    result = cur.fetchone()
                    if result:
                        # 购物车中已有该商品，更新数量
                        new_quantity = result[0] + 1
                        cur.execute("UPDATE carts SET quantity = %s WHERE user_id = %s AND goods_id = %s", (new_quantity, user_id, goods_id))
                    else:
                        # 购物车中没有该商品，插入新记录
                        cur.execute("INSERT INTO carts (user_id, goods_id, quantity) VALUES (%s, %s, 1)", (user_id, goods_id))
                    
                    # 提交事务
                    conn.commit()

        except psycopg2.Error as e:
            print("An error occurred:", e)
            if conn is not None:
                conn.close()
    
    def show_cart(self, username):
        """
        返回某个用户的购物车信息
        """
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT user_id FROM users WHERE username = %s;", (username,))
                    user_id = cur.fetchone()

                    if user_id is None:
                        print("用户不存在")
                        return [], [], [], 0

                    user_id = user_id[0]

                    # 执行查询以获取购物车详情
                    query = """
                        SELECT g.goodsname, c.quantity, g.price * g.discount, (c.quantity * g.price * g.discount) as total_price_per_item
                        FROM carts c
                        JOIN goods g ON c.goods_id = g.goods_id
                        WHERE c.user_id = %s;
                    """
                    cur.execute(query, (user_id,))

                    # 提取结果
                    cart_items = []
                    cart_total_price = 0

                    for record in cur.fetchall():
                        goods_name, quantity, price, total_price = record
                        item = {'goods_name': goods_name, 'quantity': quantity, 'price': round(price, 2), 'total_price': round(total_price, 2), 'path': f'img/{goods_name}.jpg'}
                        cart_items.append(item)
                        cart_total_price += total_price
                    return cart_items, round(cart_total_price, 2)
                
        except psycopg2.Error as e:
            print("An error occurred:", e)
            if conn is not None:
                conn.close()
            return [], 0
    
    def make_order(self, username):
        """
        用户下单
        """
        try:
            # 连接数据库
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:

                    # 获取用户ID
                    cur.execute("SELECT user_id FROM users WHERE username = %s", (username,))
                    user_id = cur.fetchone()
                    user_id = user_id[0]

                    _, cart_total_price = self.show_cart(username)
                    orderdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cur.execute("""
                        INSERT INTO orders (user_id, totalprice, orderdate) 
                        VALUES (%s, %s, %s) RETURNING order_id
                    """, (user_id, cart_total_price, orderdate))
                    order_id = cur.fetchone()[0]

                    cur.execute("SELECT goods_id, quantity FROM carts WHERE user_id = %s", (user_id,))
                    cart_items = cur.fetchall()

                    for item in cart_items:
                        goods_id, quantity = item
                        cur.execute("""
                            INSERT INTO belong_to_order (order_id, goods_id, quantity) 
                            VALUES (%s, %s, %s)
                        """, (order_id, goods_id, quantity))
                        cur.execute("""
                            SELECT sales
                            FROM goods
                            WHERE goods_id = %s
                        """, (goods_id,))
                        quantity_old = cur.fetchone()[0]
                        quantity += quantity_old
                        cur.execute("""
                            UPDATE goods
                            SET sales = %s
                            WHERE goods_id = %s
                        """, (quantity, goods_id))
                    
                    cur.execute("DELETE FROM carts WHERE user_id = %s", (user_id,))

                    # 提交事务
                    conn.commit()
                    print(f"订单 {order_id} 已创建")

        except psycopg2.DatabaseError as e:
            print(f"An error occurred: {e}")
            if conn:
                conn.close()

    def get_all_goods_for_admin(self):
        """
        展示管理员页面信息
        """
        try:
            # 连接数据库
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    # 执行查询
                    cur.execute("SELECT goodsname, typename, price, discount, sales FROM goods;")
                    # 提取结果
                    goods_items = []
                    for record in cur.fetchall():
                        goods_name, type, price, discount, sales = record
                        item = {
                            'goods_name': goods_name, 
                            'type': type, 'price': price, 
                            'path': f'img/{goods_name}.jpg', 
                            'discount': discount, 
                            'price_discount': round(price*discount, 2), 
                            'sales': sales
                        }
                        goods_items.append(item)
                    return goods_items
        except psycopg2.DatabaseError as e:
            print(f"An error occurred: {e}")
            if conn:
                conn.close()
            return []
        
    def get_goods_quantity_for_admin(self):
        """
        返回某个用户购物车商品数量
        """
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    # 查询该用户购物车中所有商品的数量
                    cur.execute("SELECT COUNT(goods_id) FROM goods")
                    total_quantity = cur.fetchone()[0]

                    return total_quantity if total_quantity is not None else 0

        except psycopg2.Error as e:
            print("An error occurred:", e)
            if conn is not None:
                conn.close()
            return -1

    def modify_goods_info_for_admin(self, goods_items):
        """
        管理员修改商品信息
        """
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    goods_names_new = []
                    for item in goods_items:
                        cur.execute("""
                            UPDATE goods
                            SET typename = %s, price = %s, discount = %s, sales = %s
                            WHERE goodsname = %s
                        """, (item['type'], item['price'], item['discount'], item['sales'], item['goods_name']))
                        goods_names_new.append(item['goods_name'])

                    cur.execute("""
                        SELECT goodsname
                        FROM goods
                    """)
                    for record in cur.fetchall():
                        goods_name = record[0]
                        if goods_name not in goods_names_new:
                            cur.execute("""
                                DELETE FROM goods CASCADE
                                WHERE goodsname = %s
                            """, (goods_name,))

                    conn.commit()

        except psycopg2.Error as e:
            print("An error occurred:", e)
            if conn is not None:
                conn.close()

    def add_goods(self, goods_name, typename, price, discount):
        """
        增加新商品
        """
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO goods(goodsname, typename, price, discount)
                        VALUES (%s, %s, %s, %s)
                    """, (goods_name, typename, price, discount))
                    print(goods_name)
                    conn.commit()

        except psycopg2.Error as e:
            print("An error occurred:", e)
            if conn is not None:
                conn.close()
    
    def get_orders(self, username):
        """
        获取某个用户的订单信息
        """
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT user_id
                        FROM users
                        WHERE username = %s
                    """, (username,))
                    user_id = cur.fetchone()[0]
                    cur.execute("""
                        SELECT order_id, totalprice, orderdate
                        FROM orders
                        WHERE user_id = %s
                    """, (user_id,))
                    order_infos = cur.fetchall()

                    order_items = []
                    for order_info in order_infos:
                        order_id = order_info[0]
                        totalprice = order_info[1]
                        orderdate = order_info[2]
                        item = {
                            'order_id': order_id, 
                            'totalprice': totalprice,
                            'orderdate': orderdate
                        }
                        cur.execute("""
                            SELECT goodsname, quantity
                            FROM belong_to_order bto
                            JOIN goods g on bto.goods_id = g.goods_id
                            WHERE bto.order_id = %s
                        """, (order_id,))
                        records = cur.fetchall()
                        goods_string = ""
                        for record in records:
                            goods_string += f"{record[0]}x{record[1]} "
                        item['goods'] = goods_string[:-1]
                        order_items.append(item)
                    return order_items
        except psycopg2.Error as e:
            print("An error occurred:", e)
            if conn is not None:
                conn.close()
            return []

    def get_all_orders_for_user(self, username):
        """
        用户界面获取所有订单信息
        """
        order_items = self.get_orders(username)
        for i in range(len(order_items)):
            order_items[i]['order_id'] = i + 1
        return order_items
    
    def get_all_orders_for_admin(self):
        """
        管理员界面获取所有订单信息
        """
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT username
                        FROM users
                    """)
                    usernames = cur.fetchall()
        except psycopg2.Error as e:
            print("An error occurred:", e)
            if conn is not None:
                conn.close()
            return []

        order_items = []
        for username in usernames:
            username = username[0]
            items = self.get_orders(username)
            for i in range(len(items)):
                items[i]['username'] = username
            order_items.extend(items)
        return order_items

        