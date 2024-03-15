from flask import render_template, session, redirect, request, url_for, send_from_directory

from .db import get_db_connection
from .api_response import ApiResponse

from werkzeug.utils import secure_filename
import os


def configure_routes(app):
    app.config['UPLOAD_FOLDER'] = 'app/static'

    @app.before_request
    def before_request():
        allowed_endpoints = ['login', 'register', 'static', 'adminlogin', ]
        if 'user_id' not in session and request.endpoint not in allowed_endpoints:
            return redirect('/login')

    @app.route('/photo/<filename>')
    def photo(filename):
        print(app.config['UPLOAD_FOLDER'])

        # 直接使用app.config['UPLOAD_FOLDER']，因为它已经设置为'app/static'，即图片存储的目录。
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @app.route('/upload-image', methods=['POST'])
    def upload_image():
        if 'photo' in request.files:
            file = request.files['photo']
            if file.filename == '':
                return ApiResponse.error("没有选中文件")

            filename = secure_filename(file.filename)

            # 确保文件被保存在static目录下
            file_path = os.path.join(app.static_folder, filename)
            file.save(file_path)

            # 使用url_for构造访问URL，确保filename参数正确指向文件名
            photo_url = url_for('static', filename=filename, _external=True)
            return ApiResponse.success("文件上传成功", {"url": photo_url})

        return ApiResponse.error("没有文件部分")

    @app.route('/images/<filename>')
    def serve_image(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @app.route('/')
    def index():
        return render_template('/index.html')

    @app.route('/adminLogin')
    def adminLogin():
        return render_template('/adminlogin.html')

    @app.route('/product_manager')
    def product_manager():
        return render_template('/product_manager.html')

    @app.route('/cart')
    def cart():
        return render_template('/cart.html')

    @app.route('/chat')
    def chat():
        return render_template('/chat.html')

    @app.route('/orders')
    def orders_tem():
        return render_template('/orders.html')

    @app.route('/product')
    def product():
        return render_template('product.html')

    @app.route('/product-detail')
    def product_detail():
        return render_template('product-detail.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    @app.route('/about-me')
    def about_me():
        return render_template('about-me.html')

    @app.route('/adminMessage')
    def adminMessage():
        return render_template('adminMessage.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            # 从表单数据中获取信息
            data = request.get_json()

            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return ApiResponse.error("邮箱和密码不能为空")

            # 连接数据库
            connection = get_db_connection()
            try:
                with connection.cursor() as cursor:
                    # 检查邮箱是否已被注册
                    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
                    existing_user = cursor.fetchone()
                    if existing_user:
                        return ApiResponse.error("用户已存在")

                    # 密码加密

                    # 插入新用户记录
                    insert_sql = "INSERT INTO users (email, password) VALUES (%s, %s)"
                    cursor.execute(insert_sql, (email, password))
                    connection.commit()

                    return ApiResponse.success()
            finally:
                connection.close()
        else:
            # 对于GET请求，显示注册页面
            return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            connection = get_db_connection()
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM users WHERE email=%s AND password=%s"
                    cursor.execute(sql, (email, password))
                    result = cursor.fetchone()

                    if result:
                        session['user_id'] = result['id']
                        return ApiResponse.success(result)
                    else:
                        return ApiResponse.error("登录失败")
            finally:
                connection.close()
        else:
            return render_template('login.html')

    @app.route('/delete-product/<int:id>', methods=['POST'])
    def delete_products(id):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                delete_sql = "DELETE FROM products WHERE id = %s"
                cursor.execute(delete_sql, (id,))
                connection.commit()
                return ApiResponse.success()
        finally:
            connection.close()

    @app.route('/update-product/<int:id>', methods=['POST'])
    def update_product(id):
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        img_src = data.get('img_src')
        category = data.get('category')
        price = data.get('price')

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                update_sql = "UPDATE products SET title = %s, description = %s, img_src = %s, category = %s, price = %s WHERE id = %s"
                cursor.execute(update_sql, (title, description, img_src, category, price, id))
                connection.commit()
                return ApiResponse.success()
        finally:
            connection.close()

    @app.route('/product_list')
    def products():
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM products")
                products = cursor.fetchall()
                return products
        finally:
            connection.close()

    @app.route('/product/<int:id>')
    def product_details(id):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
                product = cursor.fetchone()
                if product:
                    return render_template('product-detail.html', product=product)
                else:
                    return 'Product not found', 404
        finally:
            connection.close()

    @app.route('/orderslist', methods=['GET'])
    def list_orders():
        if 'user_id' not in session:
            return ApiResponse.error("用户未登录")

        user_id = session['user_id']  # 从session中获取用户ID

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 使用JOIN语句获取订单和相关商品信息
                query_sql = """
                SELECT o.order_id, o.quantity, o.unit_price, o.total_price, o.status, o.created_at,p.id,
                    p.title, p.description, p.img_src, p.category, p.price AS product_price
                FROM orders o
                JOIN products p ON o.product_id = p.id
                WHERE o.user_id = %s
                """
                cursor.execute(query_sql, (user_id,))
                orders = cursor.fetchall()

                orders_list = []
                for order in orders:
                    order_info = {
                        'order_id': order['order_id'],
                        'quantity': order['quantity'],
                        'unit_price': order['unit_price'],
                        'total_price': order['total_price'],
                        'status': order['status'],
                        'created_at': order['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
                        'product': {
                            'product_id': order['id'],
                            'title': order['title'],
                            'description': order['description'],
                            'img_src': order['img_src'],
                            'category': order['category'],
                            'price': order['product_price'],
                        }
                    }
                    orders_list.append(order_info)

                return ApiResponse.success(orders_list)
        except Exception as e:
            print(f"Error fetching orders: {e}")
            return ApiResponse.error("获取订单列表失败")
        finally:
            connection.close()

    @app.route('/create-order', methods=['POST'])
    def create_order():

        if 'user_id' not in session:
            return ApiResponse.error("用户未登录")

        # 从请求体中获取订单数据
        data = request.get_json()
        user_id = session['user_id']  # 假设用户ID已经保存在session中
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        unit_price = data.get('unit_price')
        total_price = data.get('total_price')
        status = data.get('status', 'pending')  # 默认订单状态为 'pending'

        # 连接数据库
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 插入订单记录
                insert_sql = """
                INSERT INTO orders (user_id, product_id, quantity, unit_price, total_price, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_sql, (user_id, product_id, quantity, unit_price, total_price, status))
                connection.commit()

                return ApiResponse.success("订单创建成功")
        except Exception as e:
            # 如果发生错误，打印错误信息并返回错误响应
            print(f"Error creating order: {e}")
            return ApiResponse.error("订单创建失败")
        finally:
            connection.close()

    @app.route('/add-comment', methods=['POST'])
    def add_comment():

        if 'user_id' not in session:
            return ApiResponse.error("用户未登录")

        # 从请求体中获取评论数据
        data = request.get_json()
        user_id = session['user_id']  # 从session中获取用户ID
        product_id = data.get('product_id')
        order_id = data.get('order_id')
        content = data.get('content')

        if not all([product_id, order_id, content]):
            return ApiResponse.error("评论信息不完整")

        # 连接数据库
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 插入评论记录
                insert_sql = """
                INSERT INTO comments (product_id, order_id, user_id, content)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_sql, (product_id, order_id, user_id, content))
                connection.commit()

                return ApiResponse.success("评论添加成功")
        except Exception as e:
            # 如果发生错误，打印错误信息并返回错误响应
            print(f"Error adding comment: {e}")
            return ApiResponse.error("评论添加失败")
        finally:
            connection.close()

    @app.route('/comments/<int:product_id>', methods=['GET'])
    def get_comments(product_id):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                query_sql = """
                SELECT c.comment_id, c.content, c.created_at, u.id, u.name
                FROM comments c
                JOIN users u ON c.user_id = u.id
                WHERE c.product_id = %s
                ORDER BY c.created_at DESC
                """
                cursor.execute(query_sql, (product_id,))
                comments = cursor.fetchall()

                comments_list = []
                for comment in comments:
                    comment_info = {
                        'comment_id': comment['comment_id'],
                        'content': comment['content'],
                        'created_at': comment['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
                        'user': {
                            'user_id': comment['id'],
                            'username': comment['name']
                        }
                    }
                    comments_list.append(comment_info)

                return ApiResponse.success(comments_list)
        except Exception as e:
            print(f"Error fetching comments: {e}")
            return ApiResponse.error("获取评论列表失败")
        finally:
            connection.close()

    @app.route('/add-to-cart', methods=['POST'])
    def add_to_cart():
        if 'user_id' not in session:
            return ApiResponse.error("用户未登录")

        # 从请求体中获取数据
        data = request.get_json()
        user_id = session['user_id']
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)  # 如果未提供数量，默认为1

        if not product_id:
            return ApiResponse.error("缺少商品ID")

        # 连接数据库
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 检查购物车中是否已存在同一用户和商品的项
                check_sql = "SELECT * FROM cart WHERE user_id = %s AND product_id = %s"
                cursor.execute(check_sql, (user_id, product_id))
                existing_item = cursor.fetchone()

                if existing_item:
                    # 如果已存在，更新数量
                    new_quantity = existing_item['quantity'] + quantity
                    update_sql = "UPDATE cart SET quantity = %s WHERE cart_id = %s"
                    cursor.execute(update_sql, (new_quantity, existing_item['cart_id']))
                else:
                    # 如果不存在，插入新项
                    insert_sql = "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)"
                    cursor.execute(insert_sql, (user_id, product_id, quantity))

                connection.commit()
                return ApiResponse.success("成功添加到购物车")
        except Exception as e:
            print(f"Error adding to cart: {e}")
            return ApiResponse.error("添加到购物车失败")
        finally:
            connection.close()

    @app.route('/mycart', methods=['GET'])
    def view_cart():
        if 'user_id' not in session:
            return ApiResponse.error("用户未登录")

        user_id = session['user_id']

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 查询购物车中的商品及其详细信息
                query_sql = """
                SELECT c.cart_id, c.quantity, p.id AS product_id, p.title, p.description, p.img_src, p.category, p.price
                FROM cart c
                JOIN products p ON c.product_id = p.id
                WHERE c.user_id = %s
                """
                cursor.execute(query_sql, (user_id,))
                cart_items = cursor.fetchall()

                cart_list = []
                for item in cart_items:
                    cart_info = {
                        'cart_id': item['cart_id'],
                        'quantity': item['quantity'],
                        'product': {
                            'product_id': item['product_id'],
                            'title': item['title'],
                            'description': item['description'],
                            'img_src': item['img_src'],
                            'category': item['category'],
                            'price': item['price'],
                        }
                    }
                    cart_list.append(cart_info)

                return ApiResponse.success(cart_list)
        except Exception as e:
            print(f"Error viewing cart: {e}")
            return ApiResponse.error("获取购物车失败")
        finally:
            connection.close()

    @app.route('/remove-cart-item', methods=['POST'])
    def remove_cart_item():
        if 'user_id' not in session:
            return ApiResponse.error("用户未登录")

        data = request.get_json()
        cart_id = data.get('cart_id')

        if not cart_id:
            return ApiResponse.error("缺少购物车项ID")

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                delete_sql = "DELETE FROM cart WHERE cart_id = %s AND user_id = %s"
                affected_rows = cursor.execute(delete_sql, (cart_id, session['user_id']))
                connection.commit()

                if affected_rows == 0:
                    return ApiResponse.error("移除失败，购物车项不存在")

                return ApiResponse.success("购物车项已移除")
        except Exception as e:
            print(f"Error removing cart item: {e}")
            return ApiResponse.error("移除购物车项失败")
        finally:
            connection.close()

    @app.route('/update-cart-item', methods=['POST'])
    def update_cart_item():
        if 'user_id' not in session:
            return ApiResponse.error("用户未登录")

        data = request.get_json()
        cart_id = data.get('cart_id')
        quantity = data.get('quantity')

        if not all([cart_id, quantity is not None]):
            return ApiResponse.error("缺少必要信息")

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                update_sql = "UPDATE cart SET quantity = %s WHERE cart_id = %s AND user_id = %s"
                affected_rows = cursor.execute(update_sql, (quantity, cart_id, session['user_id']))
                connection.commit()

                if affected_rows == 0:
                    return ApiResponse.error("更新失败，购物车项不存在")

                return ApiResponse.success("购物车项更新成功")
        except Exception as e:
            print(f"Error updating cart item: {e}")
            return ApiResponse.error("更新购物车项失败")
        finally:
            connection.close()

    @app.route('/submit_cart', methods=['POST'])
    def submitcar():
        if 'user_id' not in session:
            return ApiResponse.error("用户未登录")

        user_id = session['user_id']
        data = request.get_json()
        product_id = data['product_id']
        cart_id = data['cartId']
        quantity = data['quantity']
        unit_price = data['unit_price']
        total_price = data['total_price']
        status = data['status']

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                insert_sql = """
                INSERT INTO orders (user_id, product_id, quantity, unit_price, total_price, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_sql, (user_id, product_id, quantity, unit_price, total_price, status))

                clear_cart_sql = "DELETE FROM cart WHERE cart_id = %s"
                cursor.execute(clear_cart_sql, (cart_id,))
                connection.commit()

                return ApiResponse.success("订单创建成功")
        except Exception as e:
            connection.rollback()
            print(f"Error creating order: {e}")
            return ApiResponse.error("订单创建失败")
        finally:
            connection.close()

    @app.route('/send-message-to-user', methods=['POST'])
    def send_message_to_user():
        if 'admin_id' not in session:
            return ApiResponse.error("需要管理员权限")

        data = request.get_json()
        user_id = data.get('user_id')  # 获取目标用户的 ID
        message = data.get('message')  # 获取消息内容

        if not all([user_id, message]):
            return ApiResponse.error("用户 ID 和消息不能为空")

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 检查目标用户是否存在
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                if not cursor.fetchone():
                    return ApiResponse.error("目标用户不存在")

                # 检查是否已有该用户的聊天记录
                cursor.execute("SELECT chat_history FROM user_chat_history WHERE user_id = %s", (user_id,))
                record = cursor.fetchone()

                if record:
                    # 如果已存在聊天记录，则在现有记录基础上追加新消息
                    updated_history = record['chat_history'] + "\nSupport: " + message  # 假设使用换行符分隔每条消息
                    cursor.execute("UPDATE user_chat_history SET chat_history = %s WHERE user_id = %s",
                                   (updated_history, user_id))
                else:
                    # 如果不存在聊天记录，则创建新记录
                    cursor.execute("INSERT INTO user_chat_history (user_id, chat_history) VALUES (%s, %s)",
                                   (user_id, "Support: " + message))

                connection.commit()
                return ApiResponse.success("消息发送成功")
        except Exception as e:
            print(f"Error sending message to user: {e}")
            return ApiResponse.error("发送消息失败")
        finally:
            connection.close()

    @app.route('/get-all-user-chats', methods=['GET'])
    def get_all_user_chats():
        if 'admin_id' not in session:
            return ApiResponse.error("需要管理员权限")

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 查询所有用户的聊天记录
                cursor.execute(
                    "SELECT u.id, u.email, uch.chat_history FROM users u LEFT JOIN user_chat_history uch ON u.id = uch.user_id")
                records = cursor.fetchall()

                # 过滤掉聊天记录为空的用户
                filtered_records = [record for record in records if record['chat_history']]

                # 格式化聊天记录，将字符串分割为列表
                for record in filtered_records:
                    record['chat_history'] = record['chat_history'].split('\n') if record['chat_history'] else []

                return ApiResponse.success(data=filtered_records)
        except Exception as e:
            print(f"Error retrieving chat history: {e}")
            return ApiResponse.error("获取聊天记录失败")
        finally:
            connection.close()

    @app.route('/get-user-chat-history', methods=['GET'])
    def get_user_chat_history():
        if 'admin_id' not in session:
            return ApiResponse.error("需要管理员权限")

        user_id = request.args.get('user_id')  # 从查询参数中获取用户ID

        if not user_id:
            return ApiResponse.error("缺少用户ID")

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT chat_history FROM user_chat_history WHERE user_id = %s", (user_id,))
                record = cursor.fetchone()

                if record and record['chat_history']:
                    chat_history = record['chat_history'].split("\n")  # 假设聊天记录是通过换行符分隔的
                    return ApiResponse.success(chat_history)
                else:
                    return ApiResponse.success([])
        except Exception as e:
            print(f"Error fetching user chat history: {e}")
            return ApiResponse.error("获取用户聊天历史失败")
        finally:
            connection.close()

    @app.route('/get-chat-history', methods=['GET'])
    def get_chat_history():
        if 'user_id' not in session:
            return ApiResponse.error("用户未登录")

        user_id = session['user_id']

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT chat_history FROM user_chat_history WHERE user_id = %s", (user_id,))
                record = cursor.fetchone()

                if record:
                    chat_history = record['chat_history'].split("\n")
                    return ApiResponse.success(chat_history)
                else:
                    return ApiResponse.success([])
        except Exception as e:
            print(f"Error fetching chat history: {e}")
            return ApiResponse.error("获取聊天历史失败")
        finally:
            connection.close()

    @app.route('/send-message', methods=['POST'])
    def send_message():
        if 'user_id' not in session:
            return ApiResponse.error("用户未登录")

        user_id = session['user_id']
        data = request.get_json()
        message = data.get('message')

        if not message:
            return ApiResponse.error("消息不能为空")

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 检查是否已有聊天记录
                cursor.execute("SELECT chat_history FROM user_chat_history WHERE user_id = %s", (user_id,))
                record = cursor.fetchone()

                if record:
                    # 更新聊天记录
                    updated_history = record['chat_history'] + "\n" + message  # 假设使用换行符分隔每条消息
                    cursor.execute("UPDATE user_chat_history SET chat_history = %s WHERE user_id = %s",
                                   (updated_history, user_id))
                else:
                    # 创建新的聊天记录
                    cursor.execute("INSERT INTO user_chat_history (user_id, chat_history) VALUES (%s, %s)",
                                   (user_id, message))

                connection.commit()
                return ApiResponse.success("消息发送成功")
        except Exception as e:
            print(f"Error sending message: {e}")
            return ApiResponse.error("发送消息失败")
        finally:
            connection.close()

    @app.route('/adminlogin', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            connection = get_db_connection()
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM users WHERE email=%s AND password=%s"
                    cursor.execute(sql, (email, password))
                    result = cursor.fetchone()

                    print(result['role'])
                    if result and result['role'] == 'admin':
                        session['admin_id'] = result['id']
                        session['is_admin'] = True
                        return ApiResponse.success("管理员登录成功", result)
                    else:
                        return ApiResponse.error("管理员登录失败，权限不足或用户不存在")
            finally:
                connection.close()
        else:
            # 对于GET请求，返回管理员登录页面
            return render_template('admin-login.html')

    @app.route('/add-product', methods=['POST'])
    def add_product():
        # if 'admin_id' not in session:
        #     return ApiResponse.error("需要管理员权限")

        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        img_src = data.get('img_src')
        category = data.get('category')
        price = data.get('price')

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                insert_sql = "INSERT INTO products (title, description, img_src, category, price) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(insert_sql, (title, description, img_src, category, price))
                connection.commit()
                return ApiResponse.success("商品添加成功")
        finally:
            connection.close()
