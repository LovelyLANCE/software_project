CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    sex CHAR(1) CHECK (sex IN ('M', 'F', 'O')), -- 'M' 代表男性, 'F' 代表女性, 'O' 代表其他
    birthday DATE,
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(25)
);

CREATE TABLE goods (
    goods_id SERIAL PRIMARY KEY,
    typename VARCHAR(255) NOT NULL,
    goodsname VARCHAR(255) UNIQUE NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    sales INT NOT NULL DEFAULT 0,
    discount NUMERIC(3, 2) CHECK (discount >= 0 AND discount <= 1)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
	user_id INT NOT NULL,
    totalprice NUMERIC(10, 2) NOT NULL,
    orderdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE carts (
    user_id INT NOT NULL,
    goods_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (goods_id) REFERENCES goods(goods_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, goods_id)
);

CREATE TABLE belong_to_order (
    order_id INT NOT NULL,
    goods_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    PRIMARY KEY (order_id, goods_id)
);

CREATE TABLE admins (
    admin_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
