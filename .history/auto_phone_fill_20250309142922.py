import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import multiprocessing
import random
import string
import os
import re
import uuid
import sys
import requests
import json
import shutil
import signal
import atexit
import platform
import socket
import hashlib

def random_sleep(min_seconds=0.5, max_seconds=2.0):
    """随机睡眠一段时间，模拟人类行为"""
    time.sleep(random.uniform(min_seconds, max_seconds))

def clean_text(text):
    """
    去除文本中的所有空白字符（空格、制表符、换行符等）
    
    参数:
        text (str): 原始文本
    
    返回:
        str: 清理后的纯文本（不包含任何空白字符）
    """
    return ''.join(text.split())

def get_verification_code(phone_number, process_id, sid="87264"):
    """
    通过API获取手机验证码，持续轮询直到成功获取验证码
    
    参数:
        phone_number (str): 手机号码
        process_id (str): 进程ID
        sid (str): 项目ID，默认为87264
    
    返回:
        str: 验证码，如果获取失败则返回None
    """
    # API信息
    api_url = "https://api.haozhuma.cn/sms/"
    token = "12979f4ebab7cfff72c6f716a31256b673a61cb5eb74b6f000d82cbd5c1d833f7ce230aa25526a061c921eed962625876572a81c2e15f0b4a7b497091f5fb39ce355c9f42ef1ba7f5c8bf129a16585b7"
    
    # 构建请求参数
    params = {
        "api": "getMessage",
        "token": token,
        "sid": sid,
        "phone": phone_number
    }
    
    # 设置最大尝试次数和时间限制
    max_attempts = 30  # 最多尝试30次
    retry_interval = 3  # 每次尝试间隔3秒
    total_waited = 0
    max_wait_time = 120  # 最长等待时间为120秒
    
    print(f"[进程 {process_id}] 开始轮询API获取手机号 {phone_number} 的验证码...")
    
    for attempt in range(1, max_attempts + 1):
        try:
            if total_waited >= max_wait_time:
                print(f"[进程 {process_id}] 等待超过{max_wait_time}秒，获取验证码超时")
                return None
            
            print(f"[进程 {process_id}] 第{attempt}次尝试获取验证码，已等待{total_waited}秒...")
            response = requests.get(api_url, params=params)
            response_data = response.json()
            
            print(f"[进程 {process_id}] API响应: {response_data}")
            
            # 检查响应是否包含有效的验证码
            if response_data.get("code") == "0" and response_data.get("yzm"):
                verification_code = response_data.get("yzm")
                print(f"[进程 {process_id}] 成功获取验证码: {verification_code}")
                print(f"[进程 {process_id}] 短信内容: {response_data.get('sms', '无短信内容')}")
                return verification_code
            else:
                print(f"[进程 {process_id}] 尚未收到验证码，错误信息: {response_data.get('msg', '未知错误')}")
                # 等待一段时间后重试
                time.sleep(retry_interval)
                total_waited += retry_interval
        
        except Exception as e:
            print(f"[进程 {process_id}] 获取验证码时出错: {e}")
            time.sleep(retry_interval)
            total_waited += retry_interval
    
    print(f"[进程 {process_id}] 达到最大尝试次数{max_attempts}，获取验证码失败")
    return None

# 生成随机的设备指纹信息
def generate_random_fingerprint():
    """
    生成随机的设备指纹信息，用于混淆浏览器特征
    
    返回:
        dict: 包含随机设备指纹的字典
    """
    # 随机操作系统
    os_list = ["Windows NT 10.0", "Windows NT 11.0", "Macintosh; Intel Mac OS X 10_15_7", 
               "Macintosh; Intel Mac OS X 11_5_2", "X11; Linux x86_64", "X11; Ubuntu; Linux x86_64"]
    
    # 随机浏览器版本
    chrome_versions = ["110.0.5481.177", "111.0.5563.111", "112.0.5615.49", 
                       "113.0.5672.63", "114.0.5735.90", "115.0.5790.114",
                       "116.0.5845.96", "117.0.5938.62", "118.0.5993.88", "119.0.6045.105"]
    
    # 随机屏幕分辨率
    resolutions = ["1366x768", "1440x900", "1536x864", "1600x900", "1680x1050", 
                   "1920x1080", "1920x1200", "2048x1152", "2560x1440", "3440x1440", "3840x2160"]
    
    # 随机色深
    color_depths = [24, 30, 32, 48]
    
    # 随机设备内存 (GB)
    memory_sizes = [4, 8, 12, 16, 24, 32, 64]
    
    # 随机CPU核心数
    cpu_cores = [2, 4, 6, 8, 10, 12, 16, 24, 32]
    
    # 随机硬盘种类
    disk_types = ["HDD", "SSD", "NVMe SSD"]
    
    # 随机生成硬件指纹
    vendor_ids = ["0x10de", "0x8086", "0x1022", "0x1002"]
    device_ids = ["0x2204", "0x1616", "0x1521", "0x0a12", "0x0f00"]
    
    # 随机WebGL值
    webgl_vendors = ["Google Inc.", "Intel Inc.", "NVIDIA Corporation", "AMD", "ATI Technologies Inc."]
    webgl_renderers = [
        "ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (AMD, AMD Radeon RX 6800 XT Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Intel, Intel(R) Iris(R) Xe Graphics Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (NVIDIA, NVIDIA GeForce GTX 1660 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (NVIDIA, NVIDIA GeForce RTX 4070 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (AMD, AMD Radeon(TM) Graphics Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Microsoft, Microsoft Basic Render Driver Direct3D11 vs_5_0 ps_5_0)"
    ]
    
    # 随机化GPS坐标 (中国大陆主要城市范围)
    latitude = random.uniform(18.0, 53.0)
    longitude = random.uniform(73.0, 135.0)
    
    # 随机化语言偏好
    language_preferences = [
        "zh-CN,zh;q=0.9,en;q=0.8",
        "zh-CN,zh;q=0.9",
        "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6"
    ]
    
    # 随机生成MAC地址
    def generate_random_mac():
        mac = [random.randint(0x00, 0xff) for _ in range(6)]
        return ':'.join(['{:02x}'.format(x) for x in mac])
    
    # 随机生成设备ID
    device_id = str(uuid.uuid4())
    
    # 构建随机指纹数据，确保用户代理格式正确
    fingerprint = {
        "userAgent": f"Mozilla/5.0 ({random.choice(os_list)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(chrome_versions)} Safari/537.36".replace(" ", " "),
        "screenResolution": random.choice(resolutions),
        "colorDepth": random.choice(color_depths),
        "deviceMemory": random.choice(memory_sizes),
        "hardwareConcurrency": random.choice(cpu_cores),
        "diskType": random.choice(disk_types),
        "platform": random.choice(["Win32", "MacIntel", "Linux x86_64"]),
        "vendorId": random.choice(vendor_ids),
        "deviceId": random.choice(device_ids),
        "webglVendor": random.choice(webgl_vendors),
        "webglRenderer": random.choice(webgl_renderers),
        "language": random.choice(language_preferences),
        "geolocation": {
            "latitude": latitude,
            "longitude": longitude
        },
        "timezone": random.choice(["Asia/Shanghai", "Asia/Chongqing", "Asia/Harbin", "Asia/Hong_Kong"]),
        "timezoneOffset": -480,  # 中国时区偏移量
        "macAddress": generate_random_mac(),
        "uniqueId": device_id,
    }
    
    return fingerprint

def auto_fill_phone(phone_number, process_id, sid="87264"):
    """
    自动打开SiliconFlow登录页面并填写手机号
    
    参数:
        phone_number (str): 要填写的手机号码
        process_id (str): 进程唯一标识符
        sid (str): 验证码API的项目ID，默认为87264
    """    
    print(f"[进程 {process_id}] 开始为手机号 {phone_number} 自动填写表单...")
    
    # 生成随机硬件指纹
    fingerprint = generate_random_fingerprint()
    print(f"[进程 {process_id}] 为浏览器生成随机指纹: WebGL={fingerprint['webglVendor']} | 平台={fingerprint['platform']}")
    
    # 创建一个临时目录作为用户数据目录，每次使用不同的目录以隔离会话
    user_data_dir = f"chrome_user_data_{phone_number}_{process_id}"
    
    # 确保目录存在
    os.makedirs(user_data_dir, exist_ok=True)
    
    # 保存到全局列表中，以便退出时清理
    if not hasattr(auto_fill_phone, 'user_data_dirs'):
        auto_fill_phone.user_data_dirs = []
    auto_fill_phone.user_data_dirs.append(user_data_dir)
    
    # 为每个进程准备唯一的chromedriver路径
    driver_name = f"undetected_chromedriver_{process_id}.exe"
    driver_dir = os.path.join(os.path.expanduser("~"), "appdata", "local", f"undetected_{process_id}")
    os.makedirs(driver_dir, exist_ok=True)
    
    try:
        # 使用undetected_chromedriver而不是标准selenium
        options = uc.ChromeOptions()
        
        # 正确设置用户代理，确保格式正确
        user_agent = fingerprint['userAgent']
        print(f"[进程 {process_id}] 设置用户代理: {user_agent}")
        # 注意：添加参数时必须使用双引号包围整个参数，并确保没有http://前缀
        options.add_argument(f'--user-agent="{user_agent}"')
        
        # 设置用户数据目录
        options.add_argument(f"--user-data-dir={os.path.abspath(user_data_dir)}")
        
        # 设置首次运行参数，避免显示首次运行对话框
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--no-sandbox")
        
        # 增加随机性，使用随机生成的屏幕分辨率
        width, height = fingerprint['screenResolution'].split('x')
        options.add_argument(f"--window-size={width},{height}")
        
        # 设置随机窗口位置，尽量避免重叠
        position_x = random.randint(0, 300) + (int(process_id) % 5) * 100
        position_y = random.randint(0, 200) + (int(process_id) % 3) * 100
        options.add_argument(f"--window-position={position_x},{position_y}")
        
        # 增加会话隐私性
        options.add_argument("--incognito")
        
        # 禁用自动化特征 - 使用命令行参数代替experimental_options
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # 确保每个浏览器的端口不同
        debug_port = 9000 + int(process_id) % 1000
        options.add_argument(f"--remote-debugging-port={debug_port}")
        
        # 禁用扩展和GPU，提高稳定性
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        
        # 屏蔽WebRTC，防止真实IP泄露
        options.add_argument("--disable-webrtc")
        
        # 设置语言偏好
        options.add_argument(f"--lang=zh-CN")
        options.add_argument(f"--accept-lang={fingerprint['language']}")
        
        # 自定义屏幕设置
        options.add_argument(f"--color-profile={fingerprint['colorDepth']}")
        
        # 禁用共享内存用量，避免指纹追踪
        options.add_argument("--disable-dev-shm-usage")
        
        # 设置硬件并发性
        options.add_argument(f"--js-flags=--hardwareConcurrency={fingerprint['hardwareConcurrency']}")
        
        # 使用随机的设备内存
        options.add_argument(f"--js-flags=--device-memory={fingerprint['deviceMemory']}")
        
        # 初始化undetected_chromedriver，强制使用与当前Chrome版本兼容的驱动
        try:
            # 设置自定义缓存路径，避免多进程冲突
            driver = uc.Chrome(
                options=options,
                driver_executable_path=None,
                headless=False,
                version_main=133,  
                use_subprocess=True,
                user_data_dir=driver_dir  # 为每个进程设置不同的缓存目录
            )
        except Exception as chrome_error:
            if "WinError 183" in str(chrome_error):
                print(f"[进程 {process_id}] 遇到文件冲突错误，尝试备用方法...")
                
                # 尝试备用方法：如果文件已存在，随机等待后重试
                random_sleep(2.0 + random.random() * 3.0)  # 随机延迟2-5秒
                
                # 第二次尝试，使用不同的临时目录
                temp_dir = f"temp_driver_{process_id}_{random.randint(1000, 9999)}"
                os.makedirs(temp_dir, exist_ok=True)
                
                # 再次尝试初始化Chrome
                driver = uc.Chrome(
                    options=options,
                    driver_executable_path=None,
                    headless=False,
                    version_main=133,
                    use_subprocess=True,
                    user_data_dir=temp_dir,
                    browser_executable_path=None  # 尝试使用系统默认路径
                )
                
                # 如果成功，将临时目录添加到清理列表
                auto_fill_phone.user_data_dirs.append(temp_dir)
            elif "user-agent" in str(chrome_error).lower() or "http://" in str(chrome_error):
                print(f"[进程 {process_id}] 检测到用户代理设置错误，尝试备用方法...")
                # 不使用用户代理参数，直接启动浏览器
                options = uc.ChromeOptions()
                options.add_argument(f"--user-data-dir={os.path.abspath(user_data_dir)}")
                options.add_argument("--no-first-run")
                options.add_argument("--no-default-browser-check")
                options.add_argument("--no-sandbox")
                
                driver = uc.Chrome(
                    options=options,
                    driver_executable_path=None,
                    headless=False,
                    version_main=133,
                    use_subprocess=True
                )
                
                # 启动后通过JavaScript设置用户代理
                print(f"[进程 {process_id}] 通过JavaScript注入用户代理")
            else:
                # 如果是其他错误，继续向上抛出
                raise
        
        # 设置隐式等待
        driver.implicitly_wait(10)
        
        # 注入JavaScript代码来混淆浏览器指纹
        webgl_fingerprint_js = f"""
        // 覆盖WebGL指纹
        const getParameterProxyHandler = {{
            apply: function(target, thisArg, argumentsList) {{
                const paramName = argumentsList[0];
                if (paramName === 37445) {{
                    return "{fingerprint['webglVendor']}";
                }}
                if (paramName === 37446) {{
                    return "{fingerprint['webglRenderer']}";
                }}
                return Reflect.apply(target, thisArg, argumentsList);
            }}
        }};
        
        if (WebGLRenderingContext.prototype.getParameter) {{
            WebGLRenderingContext.prototype.getParameter = new Proxy(WebGLRenderingContext.prototype.getParameter, getParameterProxyHandler);
        }}
        
        if (WebGL2RenderingContext.prototype.getParameter) {{
            WebGL2RenderingContext.prototype.getParameter = new Proxy(WebGL2RenderingContext.prototype.getParameter, getParameterProxyHandler);
        }}
        
        // 覆盖Canvas指纹
        const origToDataURL = HTMLCanvasElement.prototype.toDataURL;
        HTMLCanvasElement.prototype.toDataURL = function(type) {{
            const dataURL = origToDataURL.apply(this, arguments);
            // 对Canvas数据插入轻微随机变化
            return dataURL.replace(/[a-zA-Z0-9\/+]{20,30}==/g, (match) => {{
                const rand = "{hash_val}";
                return match.substring(0, match.length-20) + rand.substring(0, 20);
            }});
        }};
        
        // 覆盖屏幕分辨率和色深
        Object.defineProperty(window.screen, 'width', {{ value: {width} }});
        Object.defineProperty(window.screen, 'height', {{ value: {height} }});
        Object.defineProperty(window.screen, 'colorDepth', {{ value: {fingerprint['colorDepth']} }});
        Object.defineProperty(window.screen, 'pixelDepth', {{ value: {fingerprint['colorDepth']} }});
        
        // 覆盖硬件并发性
        Object.defineProperty(navigator, 'hardwareConcurrency', {{ value: {fingerprint['hardwareConcurrency']} }});
        
        // 覆盖设备内存
        Object.defineProperty(navigator, 'deviceMemory', {{ value: {fingerprint['deviceMemory']} }});
        
        // 覆盖平台信息
        Object.defineProperty(navigator, 'platform', {{ value: "{fingerprint['platform']}" }});
        
        // 覆盖语言偏好
        Object.defineProperty(navigator, 'languages', {{ value: ["{fingerprint['language'].split(',')[0]}"] }});
        
        // 覆盖时区信息
        const dateProto = Date.prototype;
        const origGetTimezoneOffset = dateProto.getTimezoneOffset;
        dateProto.getTimezoneOffset = function() {{
            return {fingerprint['timezoneOffset']};
        }};
        
        // 删除webdriver属性
        if (navigator.webdriver === true) {{
            delete Object.getPrototypeOf(navigator).webdriver;
        }}
        
        // 自定义随机函数，保证不同浏览器有不同的"随机"
        const originalMathRandom = Math.random;
        const seed = {int(process_id) * random.randint(1000, 9999)};
        let counter = 0;
        Math.random = function() {{
            const x = Math.sin(seed + counter++) * 10000;
            return x - Math.floor(x);
        }};
        """
        
        # 生成唯一的哈希值，用于Canvas指纹混淆
        hash_val = hashlib.md5(f"{phone_number}_{process_id}_{random.random()}".encode()).hexdigest()
        webgl_fingerprint_js = webgl_fingerprint_js.replace('{hash_val}', hash_val)
        
        # 在网页加载前注入JavaScript代码
        driver.get("about:blank")
        driver.execute_script(webgl_fingerprint_js)
        
        # 打开硅基流动登录页面 - 确保使用正确的URL
        login_url = "https://account.siliconflow.cn/zh/login?redirect=https%3A%2F%2Fcloud.siliconflow.cn%2F%3F"
        print(f"[进程 {process_id}] 正在打开硅基流动登录页面: {login_url}")
        driver.get(login_url)
        print(f"[进程 {process_id}] 已为手机号 {phone_number} 打开登录页面")
        
        # 随机延迟，模拟人类阅读页面
        random_sleep(1.0, 2.0)
        
        # 尝试找到并填写手机号输入框
        try:
            # 确认页面已正确加载
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='tel' or contains(@placeholder, '请输入手机号')]"))
            )
            
            # 尝试通过各种选择器找到输入框
            selectors = [
                "//input[@placeholder='请输入手机号' or contains(@placeholder, '手机号')]",
                "//input[contains(@class, 'phone') or contains(@name, 'phone') or contains(@id, 'phone')]",
                "//input[@type='tel']"
            ]
            
            phone_input = None
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    if elements:
                        phone_input = elements[0]
                        break
                except:
                    continue
            
            if not phone_input:
                print(f"[进程 {process_id}] 未找到手机号输入框，尝试查看页面源码...")
                print(driver.page_source)
                return
            
            # 直接点击输入框
            phone_input.click()
            
            # 清空输入框
            phone_input.clear()
            
            # 直接输入手机号，不再模拟人类输入
            phone_input.send_keys(phone_number)
            
            print(f"[进程 {process_id}] 已成功填写手机号: {phone_number}")
            
            # 尝试找到并点击复选框
            random_sleep(0.5, 1.0)
            
            try:
                # 使用多种选择器尝试找到复选框
                checkbox_selectors = [
                    "//input[@class='ant-checkbox-input' and @type='checkbox']",
                    "//span[contains(@class, 'ant-checkbox')]/input[@type='checkbox']",
                    "//input[@type='checkbox']",
                    "//label[contains(@class, 'ant-checkbox-wrapper')]//input"
                ]
                
                checkbox = None
                for selector in checkbox_selectors:
                    try:
                        checkbox_elements = driver.find_elements(By.XPATH, selector)
                        if checkbox_elements:
                            checkbox = checkbox_elements[0]
                            break
                    except:
                        continue
                
                if checkbox:
                    # 创建动作链
                    action = ActionChains(driver)
                    # 移动到复选框并点击
                    action.move_to_element(checkbox).click().perform()
                    print(f"[进程 {process_id}] 已点击复选框")
                    random_sleep(0.5, 1.0)
                else:
                    # 如果没有找到复选框，尝试点击复选框的父元素
                    try:
                        checkbox_containers = driver.find_elements(By.XPATH, "//span[contains(@class, 'ant-checkbox')]")
                        if checkbox_containers:
                            action = ActionChains(driver)
                            action.move_to_element(checkbox_containers[0]).click().perform()
                            print(f"[进程 {process_id}] 已点击复选框容器")
                            random_sleep(0.5, 1.0)
                        else:
                            print(f"[进程 {process_id}] 未找到复选框元素")
                    except Exception as e:
                        print(f"[进程 {process_id}] 点击复选框容器时出错: {e}")
            except Exception as e:
                print(f"[进程 {process_id}] 尝试尝试点击复选框时出错: {e}")
            
            # 尝试点击获取验证码按钮并自动填写验证码
            try:
                # 等待页面充分加载，但减少等待时间
                random_sleep(0.5, 1.0)
                
                print(f"[进程 {process_id}] 开始查找验证码按钮...")
                
                # 优先使用最精确的选择器，减少选择器数量
                code_button_selectors = [
                    # 完全匹配用户提供的HTML结构
                    "//button[@type='button' and contains(@class, 'ant-btn') and contains(@class, 'ant-btn-link')]/span[text()='获取验证码']/parent::button",
                    "//button[contains(@class, 'ant-btn-link')]/span[text()='获取验证码']/parent::button",
                    # 模糊匹配作为备用
                    "//button[contains(@class, 'ant-btn')]/span[contains(text(), '获取验证码')]/parent::button",
                    "//button[contains(text(), '验证码') or contains(text(), '获取')]"
                ]
                
                # 直接查找验证码按钮，跳过其他检查
                code_button = None
                for selector in code_button_selectors:
                    try:
                        elements = driver.find_elements(By.XPATH, selector)
                        if elements:
                            code_button = elements[0]
                            print(f"[进程 {process_id}] 已找到验证码按钮: {selector}")
                            break
                    except Exception as e:
                        continue
                
                if code_button:
                    # 快速检查按钮是否可点击
                    is_button_disabled = False
                    try:
                        disabled_attr = code_button.get_attribute("disabled")
                        is_button_disabled = disabled_attr == "true" or disabled_attr == "disabled"
                    except:
                        pass
                    
                    if not is_button_disabled:
                        # 直接使用JavaScript点击，这通常是最快的方法
                        try:
                            driver.execute_script("arguments[0].click();", code_button)
                            print(f"[进程 {process_id}] 已点击获取验证码按钮")
                            
                            # 减少等待时间，更快开始获取验证码
                            random_sleep(2.0, 3.0)
                            
                            # 通过API获取验证码
                            verification_code = get_verification_code(phone_number, process_id, sid)
                            
                            if verification_code:
                                # 查找验证码输入框
                                code_input_selectors = [
                                    "//input[contains(@placeholder, '验证码')]",
                                    "//input[contains(@class, 'code') or contains(@name, 'code') or contains(@id, 'code')]",
                                    "//div[contains(text(), '验证码') or contains(text(), '短信')]/following::input[1]",
                                    "//label[contains(text(), '验证码')]/following::input[1]"
                                ]
                                
                                code_input = None
                                for selector in code_input_selectors:
                                    try:
                                        code_inputs = driver.find_elements(By.XPATH, selector)
                                        if code_inputs:
                                            code_input = code_inputs[0]
                                            print(f"[进程 {process_id}] 已找到验证码输入框: {selector}")
                                            break
                                    except Exception as e:
                                        print(f"[进程 {process_id}] 查找验证码输入框出错: {e}")
                                
                                if code_input:
                                    try:
                                        # 输入验证码前先清空输入框
                                        code_input.click()
                                        code_input.clear()
                                        
                                        # 输入验证码，模拟人工输入
                                        print(f"[进程 {process_id}] 开始输入验证码: {verification_code}")
                                        for digit in verification_code:
                                            code_input.send_keys(digit)
                                            random_sleep(0.1, 0.3)
                                        
                                        print(f"[进程 {process_id}] 已输入验证码: {verification_code}")
                                        
                                        # 等待一会，确保验证码被正确接收
                                        random_sleep(1.0, 2.0)
                                        
                                        # 尝试查找并点击登录/提交按钮
                                        submit_button_selectors = [
                                            "//button[contains(@type, 'submit')]",
                                            "//button[contains(text(), '登录') or contains(text(), '注册') or contains(text(), '提交')]",
                                            "//div[contains(text(), '登录')]/parent::button",
                                            "//span[contains(text(), '登录')]/parent::button",
                                            "//button[contains(@class, 'submit') or contains(@class, 'login')]"
                                        ]
                                        
                                        submit_button = None
                                        for selector in submit_button_selectors:
                                            try:
                                                submit_buttons = driver.find_elements(By.XPATH, selector)
                                                if submit_buttons:
                                                    submit_button = submit_buttons[0]
                                                    print(f"[进程 {process_id}] 已找到登录/提交按钮: {selector}")
                                                    break
                                            except Exception as e:
                                                print(f"[进程 {process_id}] 查找登录/提交按钮出错: {e}")
                                        
                                        if submit_button:
                                            random_sleep(1.0, 2.0)
                                            
                                            # 使用JavaScript点击可能更可靠
                                            try:
                                                driver.execute_script("arguments[0].click();", submit_button)
                                                print(f"[进程 {process_id}] 已使用JavaScript点击登录/提交按钮")
                                            except Exception as js_err:
                                                print(f"[进程 {process_id}] JavaScript点击登录按钮失败: {js_err}")
                                                # 如果JavaScript点击失败，尝试常规点击
                                                action = ActionChains(driver)
                                                action.move_to_element(submit_button).click().perform()
                                                print(f"[进程 {process_id}] 已使用ActionChains点击登录/提交按钮")
                                            
                                            print(f"[进程 {process_id}] 登录流程完成")
                                            
                                            # 等待登录成功后的页面加载，减少等待时间
                                            print(f"[进程 {process_id}] 等待页面加载完成...")
                                            random_sleep(1.0, 1.5)  # 减少等待时间
                                            
                                            # 一次性完成所有三个步骤，使用更简洁的JavaScript实现
                                            try:
                                                print(f"[进程 {process_id}] 开始执行API密钥创建流程...")
                                                
                                                # 使用单一JavaScript操作完成所有步骤，避免多次元素查找
                                                js_api_key_flow = f"""
                                                (function() {{
                                                    // 获取当前页面URL，判断当前状态
                                                    var currentUrl = window.location.href;
                                                    var isAPIKeyPage = currentUrl.includes('account/ak');
                                                    var hasModal = document.querySelector('.ant-modal-content') !== null;
                                                    
                                                    // 根据不同状态执行不同步骤
                                                    if (hasModal) {{
                                                        console.log('模态框已显示，直接执行步骤3');
                                                        // 填写描述并点击提交
                                                        completeStep3("{description_text}");
                                                        return 3; // 返回执行的步骤
                                                    }} else if (isAPIKeyPage) {{
                                                        console.log('已在API密钥页面，执行步骤2-3');
                                                        // 点击新建按钮并填写描述
                                                        if (completeStep2()) {{
                                                            setTimeout(function() {{
                                                                completeStep3("{description_text}");
                                                            }}, 800);
                                                        }}
                                                        return 2; // 返回执行的步骤
                                                    }} else {{
                                                        console.log('执行完整流程步骤1-2-3');
                                                        // 执行完整流程
                                                        if (completeStep1()) {{
                                                            setTimeout(function() {{
                                                                if (completeStep2()) {{
                                                                    setTimeout(function() {{
                                                                        completeStep3("{description_text}");
                                                                    }}, 800);
                                                                }}
                                                            }}, 800);
                                                        }}
                                                        return 1; // 返回执行的步骤
                                                    }}
                                                    
                                                    // 步骤1：点击API密钥菜单
                                                    function completeStep1() {{
                                                        // 直接查找API密钥菜单元素
                                                        var apiMenuItems = document.querySelectorAll('li.ant-menu-item');
                                                        for (var i = 0; i < apiMenuItems.length; i++) {{
                                                            if (apiMenuItems[i].textContent.includes('API') || 
                                                                apiMenuItems[i].innerHTML.includes('svg')) {{
                                                                console.log('找到API密钥菜单，点击');
                                                                apiMenuItems[i].click();
                                                                return true;
                                                            }}
                                                        }}
                                                        return false;
                                                    }}
                                                    
                                                    // 步骤2：点击新建API密钥按钮
                                                    function completeStep2() {{
                                                        // 直接查找新建API密钥按钮
                                                        var buttons = document.querySelectorAll('button');
                                                        for (var i = 0; i < buttons.length; i++) {{
                                                            if (buttons[i].textContent.includes('新建 API 密钥')) {{
                                                                console.log('找到新建API密钥按钮，点击');
                                                                buttons[i].click();
                                                                return true;
                                                            }}
                                                        }}
                                                        return false;
                                                    }}
                                                    
                                                    // 步骤3：在模态框中填写描述并点击新建密钥
                                                    function completeStep3(description) {{
                                                        // 查找描述输入框
                                                        var descInput = document.getElementById('description');
                                                        if (!descInput) {{
                                                            var inputs = document.querySelectorAll('input[placeholder*="描述"]');
                                                            if (inputs.length > 0) descInput = inputs[0];
                                                        }}
                                                        
                                                        if (descInput) {{
                                                            // 设置描述值
                                                            console.log('设置描述: ' + description);
                                                            descInput.value = description;
                                                            descInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                                                            
                                                            // 查找并点击确认按钮
                                                            setTimeout(function() {{
                                                                var modalFooter = document.querySelector('.ant-modal-footer');
                                                                if (modalFooter) {{
                                                                    var confirmButtons = modalFooter.querySelectorAll('button');
                                                                    var primaryButton = null;
                                                                    
                                                                    // 找到主按钮（通常是最后一个或带有primary类的按钮）
                                                                    for (var i = 0; i < confirmButtons.length; i++) {{
                                                                        if (confirmButtons[i].className.includes('primary') || 
                                                                            confirmButtons[i].textContent.includes('新建密钥')) {{
                                                                            primaryButton = confirmButtons[i];
                                                                            break;
                                                                        }}
                                                                    }}
                                                                    
                                                                    // 如果找不到，使用最后一个按钮
                                                                    if (!primaryButton && confirmButtons.length > 0) {{
                                                                        primaryButton = confirmButtons[confirmButtons.length-1];
                                                                    }}
                                                                    
                                                                    if (primaryButton) {{
                                                                        console.log('点击确认按钮');
                                                                        primaryButton.click();
                                                                        return true;
                                                                    }}
                                                                }}
                                                                return false;
                                                            }}, 300);
                                                            return true;
                                                        }}
                                                        return false;
                                                    }}
                                                }})();
                                                """
                                                
                                                # 执行整合的JavaScript流程
                                                result = driver.execute_script(js_api_key_flow)
                                                if result == 1:
                                                    print(f"[进程 {process_id}] 已启动完整API密钥创建流程（步骤1-2-3）")
                                                elif result == 2:
                                                    print(f"[进程 {process_id}] 已启动步骤2-3（在API密钥页面创建新密钥）")
                                                elif result == 3:
                                                    print(f"[进程 {process_id}] 已完成步骤3（提交模态框）")
                                                
                                                # 等待流程执行完成（较短的等待时间）
                                                print(f"[进程 {process_id}] 等待API密钥创建完成...")
                                                random_sleep(2.0, 3.0)
                                                
                                                # 检查是否成功（可选，不中断流程）
                                                try:
                                                    success_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'ant-message-success')]")
                                                    if success_elements:
                                                        print(f"[进程 {process_id}] 检测到成功消息，API密钥创建成功")
                                                except:
                                                    pass
                                                
                                                print(f"[进程 {process_id}] API密钥创建流程执行完毕")
                                                
                                            except Exception as api_key_error:
                                                print(f"[进程 {process_id}] 创建API密钥过程中出错: {api_key_error}")
                                                # 简单的备用方法（如果JavaScript方法失败）
                                                try:
                                                    print(f"[进程 {process_id}] 尝试使用备用Selenium方法...")
                                                    
                                                    # 步骤1: 使用快速精确的选择器点击API密钥菜单
                                                    try:
                                                        menu_item = driver.find_element(By.XPATH, "//li[contains(@class, 'ant-menu-item')]//span[text()='API 密钥']/parent::li")
                                                        driver.execute_script("arguments[0].click();", menu_item)
                                                        random_sleep(0.5, 1.0)
                                                    except:
                                                        print(f"[进程 {process_id}] 尝试点击API密钥菜单失败，继续后续步骤")
                                                    
                                                    # 步骤2: 使用快速精确的选择器点击新建API密钥按钮
                                                    try:
                                                        create_button = driver.find_element(By.XPATH, "//button/span[text()='新建 API 密钥']/parent::button")
                                                        driver.execute_script("arguments[0].click();", create_button)
                                                        random_sleep(0.5, 1.0)
                                                    except:
                                                        print(f"[进程 {process_id}] 尝试点击新建API密钥按钮失败，继续后续步骤")
                                                    
                                                    # 步骤3: 填写描述并点击确认
                                                    try:
                                                        # 查找描述输入框
                                                        desc_input = driver.find_element(By.ID, "description")
                                                        desc_input.clear()
                                                        desc_input.send_keys(f"Auto API Key - {phone_number}")
                                                        
                                                        # 点击确认按钮
                                                        confirm_button = driver.find_element(By.XPATH, "//div[contains(@class, 'ant-modal-footer')]//button[contains(@class, 'ant-btn-primary')]")
                                                        driver.execute_script("arguments[0].click();", confirm_button)
                                                    except:
                                                        print(f"[进程 {process_id}] 尝试填写表单并提交失败")
                                                except Exception as backup_error:
                                                    print(f"[进程 {process_id}] 备用方法也失败: {backup_error}")
                                        else:
                                            print(f"[进程 {process_id}] 登录流程完成")
                                    except Exception as input_err:
                                        print(f"[进程 {process_id}] 输入验证码时出错: {input_err}")
                                else:
                                    print(f"[进程 {process_id}] 未找到验证码输入框")
                            else:
                                print(f"[进程 {process_id}] 未能获取验证码，流程无法继续")
                        except Exception as js_error:
                            # JavaScript点击失败时使用其他方法
                            try:
                                code_button.click()
                                print(f"[进程 {process_id}] 已通过直接点击获取验证码按钮")
                            except:
                                action = ActionChains(driver)
                                action.move_to_element(code_button).click().perform()
                                print(f"[进程 {process_id}] 已通过ActionChains点击获取验证码按钮")
                            
                            random_sleep(2.0, 3.0)
                            verification_code = get_verification_code(phone_number, process_id, sid)
                            
                            if verification_code:
                                # 查找验证码输入框
                                code_input_selectors = [
                                    "//input[contains(@placeholder, '验证码')]",
                                    "//input[contains(@class, 'code') or contains(@name, 'code') or contains(@id, 'code')]",
                                    "//div[contains(text(), '验证码') or contains(text(), '短信')]/following::input[1]",
                                    "//label[contains(text(), '验证码')]/following::input[1]"
                                ]
                                
                                code_input = None
                                for selector in code_input_selectors:
                                    try:
                                        code_inputs = driver.find_elements(By.XPATH, selector)
                                        if code_inputs:
                                            code_input = code_inputs[0]
                                            print(f"[进程 {process_id}] 已找到验证码输入框: {selector}")
                                            break
                                    except Exception as e:
                                        print(f"[进程 {process_id}] 查找验证码输入框出错: {e}")
                                
                                if code_input:
                                    try:
                                        # 输入验证码前先清空输入框
                                        code_input.click()
                                        code_input.clear()
                                        
                                        # 输入验证码，模拟人工输入
                                        print(f"[进程 {process_id}] 开始输入验证码: {verification_code}")
                                        for digit in verification_code:
                                            code_input.send_keys(digit)
                                            random_sleep(0.1, 0.3)
                                        
                                        print(f"[进程 {process_id}] 已输入验证码: {verification_code}")
                                        
                                        # 等待一会，确保验证码被正确接收
                                        random_sleep(1.0, 2.0)
                                        
                                        # 尝试查找并点击登录/提交按钮
                                        submit_button_selectors = [
                                            "//button[contains(@type, 'submit')]",
                                            "//button[contains(text(), '登录') or contains(text(), '注册') or contains(text(), '提交')]",
                                            "//div[contains(text(), '登录')]/parent::button",
                                            "//span[contains(text(), '登录')]/parent::button",
                                            "//button[contains(@class, 'submit') or contains(@class, 'login')]"
                                        ]
                                        
                                        submit_button = None
                                        for selector in submit_button_selectors:
                                            try:
                                                submit_buttons = driver.find_elements(By.XPATH, selector)
                                                if submit_buttons:
                                                    submit_button = submit_buttons[0]
                                                    print(f"[进程 {process_id}] 已找到登录/提交按钮: {selector}")
                                                    break
                                            except Exception as e:
                                                print(f"[进程 {process_id}] 查找登录/提交按钮出错: {e}")
                                        
                                        if submit_button:
                                            random_sleep(1.0, 2.0)
                                            
                                            # 使用JavaScript点击可能更可靠
                                            try:
                                                driver.execute_script("arguments[0].click();", submit_button)
                                                print(f"[进程 {process_id}] 已使用JavaScript点击登录/提交按钮")
                                            except Exception as js_err:
                                                print(f"[进程 {process_id}] JavaScript点击登录按钮失败: {js_err}")
                                                # 如果JavaScript点击失败，尝试常规点击
                                                action = ActionChains(driver)
                                                action.move_to_element(submit_button).click().perform()
                                                print(f"[进程 {process_id}] 已使用ActionChains点击登录/提交按钮")
                                            
                                            print(f"[进程 {process_id}] 登录流程完成")
                                        else:
                                            print(f"[进程 {process_id}] 未找到登录/提交按钮")
                                    except Exception as input_err:
                                        print(f"[进程 {process_id}] 输入验证码时出错: {input_err}")
                                else:
                                    print(f"[进程 {process_id}] 未找到验证码输入框")
                            else:
                                print(f"[进程 {process_id}] 未能获取验证码，流程无法继续")
                    else:
                        print(f"[进程 {process_id}] 获取验证码按钮被禁用，可能在倒计时")
                else:
                    print(f"[进程 {process_id}] 未找到获取验证码按钮，尝试打印页面元素...")
                    # 打印页面上所有按钮的HTML，帮助调试
                    buttons = driver.find_elements(By.TAG_NAME, "button")
                    print(f"[进程 {process_id}] 页面上找到 {len(buttons)} 个按钮元素:")
                    for i, btn in enumerate(buttons):
                        try:
                            btn_html = btn.get_attribute("outerHTML")
                            btn_text = btn.text
                            print(f"按钮 {i+1}: {btn_text} - HTML: {btn_html}")
                        except:
                            pass
            except Exception as e:
                print(f"[进程 {process_id}] 处理验证码时出错: {e}")
                
        except Exception as e:
            print(f"[进程 {process_id}] 填写手机号时出错: {e}")
            
            # 如果上面的方法失败，可以尝试打印页面源代码帮助调试
            print(f"[进程 {process_id}] 页面源代码:")
            print(driver.page_source)
            
    except Exception as e:
        print(f"[进程 {process_id}] 浏览器操作出错: {e}")
        # 提供更具体的错误处理建议
        if "WinError 183" in str(e):
            print(f"[进程 {process_id}] 提示: 这是由于多个进程同时操作chromedriver文件导致的冲突，请尝试:")
            print(f"  1. 关闭所有Chrome浏览器和相关进程")
            print(f"  2. 删除 %APPDATA%\\undetected_chromedriver 目录")
            print(f"  3. 重新运行脚本，减少同时启动的进程数量")
        
    print(f"[进程 {process_id}] 手机号 {phone_number} 脚本执行完毕")
    
    # 保持进程运行，不关闭浏览器
    while True:
        try:
            time.sleep(1000)
        except KeyboardInterrupt:
            print(f"[进程 {process_id}] 接收到终止信号")
            break

def open_multiple_browsers(phone_numbers, sid="87264"):
    """
    使用多进程打开多个浏览器实例并填写不同的手机号
    
    参数:
        phone_numbers (list): 要填写的手机号列表
        sid (str): 验证码API的项目ID，默认为87264
    """
    processes = []
    
    # 为每个手机号创建一个进程
    for i, phone in enumerate(phone_numbers):
        # 为每个进程分配一个ID
        process_id = str(i + 1)
        
        # 创建进程
        process = multiprocessing.Process(
            target=auto_fill_phone, 
            args=(phone, process_id, sid)
        )
        
        processes.append(process)
    
    # 按批次启动进程以避免资源竞争
    batch_size = 2  # 每批启动的进程数
    total_batches = (len(processes) + batch_size - 1) // batch_size
    
    for batch in range(total_batches):
        start_idx = batch * batch_size
        end_idx = min(start_idx + batch_size, len(processes))
        
        print(f"正在启动第 {batch+1}/{total_batches} 批浏览器实例 ({start_idx+1}-{end_idx})...")
        
        # 启动当前批次的进程
        for i in range(start_idx, end_idx):
            processes[i].start()
            # 每个浏览器启动间隔随机延迟更长时间，避免资源冲突
            time.sleep(random.uniform(8.0, 10.0))
    
    print(f"已启动 {len(processes)} 个浏览器进程")
    return processes

def extract_phone_numbers_from_clean_text(text):
    """
    从完全清理后的文本中提取手机号（逐字符扫描方法）
    
    参数:
        text (str): 已清理的文本（无空白字符）
    
    返回:
        list: 提取到的手机号列表
    """
    # 存储找到的手机号
    found_phones = []
    
    # 逐字符扫描文本
    i = 0
    while i <= len(text) - 11:  # 需要至少11个字符才能形成手机号
        # 检查当前位置开始的11个字符是否是手机号
        potential_phone = text[i:i+11]
        
        # 检查是否符合中国大陆手机号的格式（1开头的11位数字）
        if potential_phone[0] == '1' and potential_phone.isdigit():
            # 进一步验证第二位是否在3-9之间
            if '3' <= potential_phone[1] <= '9':
                found_phones.append(potential_phone)
                print(f"在位置 {i} 找到手机号: {potential_phone}")
                
                # 跳过这个手机号的剩余部分
                i += 11
                continue
        
        # 移动到下一个字符
        i += 1
    
    # 去除重复的手机号
    unique_phones = list(set(found_phones))
    return unique_phones

# 在脚本退出时清理所有临时目录
def cleanup_temp_directories():
    """清理所有临时Chrome用户数据目录"""
    print("\n正在清理临时目录...")
    
    # 从auto_fill_phone函数获取保存的目录列表
    if hasattr(auto_fill_phone, 'user_data_dirs'):
        for directory in auto_fill_phone.user_data_dirs:
            try:
                if os.path.exists(directory):
                    print(f"删除目录: {directory}")
                    shutil.rmtree(directory, ignore_errors=True)
            except Exception as e:
                print(f"删除目录 {directory} 时出错: {e}")
    
    # 额外搜索可能遗留的临时目录
    try:
        for item in os.listdir('.'):
            if os.path.isdir(item) and item.startswith('chrome_user_data_'):
                try:
                    print(f"删除遗留目录: {item}")
                    shutil.rmtree(item, ignore_errors=True)
                except Exception as e:
                    print(f"删除遗留目录 {item} 时出错: {e}")
    except Exception as e:
        print(f"搜索遗留目录时出错: {e}")
    
    print("清理完成")

if __name__ == "__main__":
    # 确保脚本使用多进程模式启动
    multiprocessing.freeze_support()
    
    # 注册退出时的清理函数
    atexit.register(cleanup_temp_directories)
    
    # 添加信号处理程序，确保在Ctrl+C时也能清理
    def signal_handler(sig, frame):
        print("\n接收到中断信号，准备清理...")
        cleanup_temp_directories()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    print("SiliconFlow手机号自动填写工具 (多进程版)")
    print("=" * 50)
    print("请输入或粘贴包含手机号的文本")
    print("输入完成后，请键入'end'然后按回车结束输入")
    print("这样可以确保处理所有数据，即使其中包含空行")
    print("=" * 50)
    
    # 收集输入（直到遇到特定结束标记）
    lines = []
    print("请开始输入文本（输入'end'结束）：")
    while True:
        try:
            line = input()
            if line.strip() == "end":
                break
            lines.append(line)
        except EOFError:  # 处理EOF（Ctrl+D/Ctrl+Z）
            break
    
    # 合并所有输入行
    input_text = "\n".join(lines)
    
    # 显示原始文本
    print("\n您输入的原始文本是：")
    print("-" * 50)
    print(input_text)
    print("-" * 50)
    print(f"原始文本长度: {len(input_text)} 字符")
    print(f"原始文本行数: {len(lines)} 行")
    
    # 清理文本（去除所有空格和换行）
    cleaned_text = clean_text(input_text)
    print(f"\n清理后的文本长度: {len(cleaned_text)} 字符")
    print("所有空格、换行和空白字符已移除")
    
    # 从清理后的文本中提取手机号
    phone_numbers = extract_phone_numbers_from_clean_text(cleaned_text)
    
    # 检查是否找到手机号
    if not phone_numbers:
        print("未在输入文本中找到有效的手机号！")
        sys.exit(1)
    
    # 显示找到的手机号
    print(f"\n成功提取到 {len(phone_numbers)} 个手机号:")
    for i, phone in enumerate(phone_numbers):
        print(f"{i+1}. {phone}")
    
    # 项目ID已设置为固定值87264
    sid = "87264"
    print(f"\n验证码API的项目ID(sid)已设置为: {sid}")
    
    # 删除询问是否继续的代码，直接启动浏览器
    print(f"\n正在为 {len(phone_numbers)} 个手机号启动独立的浏览器进程...")
    processes = open_multiple_browsers(phone_numbers, sid)
    
    # 输出提示信息
    print("\n所有浏览器已启动完成，每个浏览器在独立的进程中运行")
    print("这些浏览器会一直保持运行，直到您手动关闭它们")
    print("您可以按Ctrl+C终止此脚本，浏览器仍会保持运行")
    print("或者您可以直接关闭浏览器窗口")
    
    # 等待用户手动终止
    try:
        # 主进程保持运行，但不阻塞浏览器进程
        while True:
            time.sleep(60)
            # 检查子进程状态，更新存活进程数
            running_processes = [p for p in processes if p.is_alive()]
            if len(running_processes) < len(processes):
                print(f"当前有 {len(running_processes)}/{len(processes)} 个浏览器进程在运行")
                processes = running_processes
                
            if not running_processes:
                print("所有浏览器进程已关闭，脚本结束")
                break
    except KeyboardInterrupt:
        print("\n主脚本已终止，浏览器进程会继续运行")
    finally:
        # 确保在任何情况下退出前都执行清理
        cleanup_temp_directories()
    
    print("感谢使用！") 