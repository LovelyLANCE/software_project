# import pytest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# from selenium.webdriver.chrome.options import Options

# @pytest.fixture(scope="module")
# def driver():
#     # 使用 ChromeDriverManager 自动下载和安装 ChromeDriver
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('--remote-debugging-port=9222')
#     # service = ChromeService(ChromeDriverManager().install())
#     driver = webdriver.Remote(
#         command_executor='http://selenium:4444/wd/hub',
#         options=options
#     )
#     yield driver
#     driver.quit()

# def test_login(client, driver):
#     driver.get("http://localhost:5000/login")  # 使用硬编码的 localhost 地址和端口号

#     username_input = driver.find_element(By.NAME, "username")
#     password_input = driver.find_element(By.NAME, "password")
#     submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")

#     username_input.send_keys("testuser")
#     password_input.send_keys("encrypted_password_example")
#     submit_button.click()

#     time.sleep(2)  # 等待页面加载

#     # 检查登录结果
#     assert "Invalid username or password" not in driver.page_source, "Login failed with error message."
#     assert driver.current_url == "http://localhost:5000/index", "Login did not redirect to the index page."





# def test_selenium_register(driver, live_server):
#     driver.get(live_server.url + "/register")

#     username_field = driver.find_element(By.NAME, "username")
#     password_field = driver.find_element(By.NAME, "password")
#     email_field = driver.find_element(By.NAME, "email")
#     sex_field = driver.find_element(By.NAME, "sex")
#     birthday_field = driver.find_element(By.NAME, "birthday")
#     address_field = driver.find_element(By.NAME, "address")
#     phone_field = driver.find_element(By.NAME, "phone")
#     submit_button = driver.find_element(By.NAME, "submit")

#     unique_username = f'newuser3_{int(time.time())}'

#     username_field.send_keys(unique_username)
#     password_field.send_keys("password123")
#     email_field.send_keys("newuser@example.com")
#     sex_field.send_keys("M")
#     birthday_field.send_keys("1990-01-01")
#     address_field.send_keys("123 Main St")
#     phone_field.send_keys("1234567890")
#     submit_button.click()

#     # 验证是否成功注册
#     success_message = driver.find_element(By.ID, "success-message")
#     assert success_message is not None



# driver.get(live_server.url + "/login")

    # username_field = driver.find_element(By.NAME, "username")
    # password_field = driver.find_element(By.NAME, "password")
    # submit_button = driver.find_element(By.NAME, "submit")

    # username_field.send_keys("lz")
    # password_field.send_keys("123456")
    # submit_button.click()

    # # 验证是否成功登录
    # success_message = driver.find_element(By.ID, "success-message")
    # assert success_message is not None

# import pytest
# import requests
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from flask_testing import LiveServerTestCase
# from emall.app import create_app
# from emall.database import Database

# class MyTest(LiveServerTestCase):
#     def create_app(self):
#         app = create_app()
#         app.config['TESTING'] = True
#         app.config['LIVESERVER_PORT'] = 8943
#         return app

#     def setUp(self):
#         options = webdriver.ChromeOptions()
#         options.add_argument('--headless')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')
#         # options.add_argument('--remote-debugging-port=9222')
#         # service = ChromeService(ChromeDriverManager().install())
#         self.driver = webdriver.Remote(
#             command_executor='http://selenium:4444/wd/hub',
#             options=options
#         )
#         self.wait_for_server()

#     def tearDown(self):
#         self.driver.quit()
    
#     def wait_for_server(self):
#         url = self.get_server_url()
#         timeout = 60  # 等待最长时间（秒）
#         start_time = time.time()
#         while True:
#             try:
#                 response = requests.get(url)
#                 if response.status_code == 200:
#                     break
#             except requests.exceptions.ConnectionError:
#                 pass
#             if time.time() - start_time > timeout:
#                 raise Exception("Server did not start within the timeout period")
#             time.sleep(1)

#     def test_login(self):
#         self.driver.get(self.get_server_url() + "/login")
#         assert "登录" in self.driver.title

#         username_field = self.driver.find_element(By.NAME, "username")
#         password_field = self.driver.find_element(By.NAME, "password")
#         login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

#         username_field.send_keys("testuser")
#         password_field.send_keys("testpassword")
#         login_button.click()

#         assert "首页" in self.driver.title

# if __name__ == "__main__":
#     pytest.main()

def test_admin_orders(client):
    with client.session_transaction() as sess:
        sess['adminname'] = 'admin'
    response = client.get('/admin/order')
    assert response.status_code == 200