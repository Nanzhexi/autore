import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import threading
import random
import string
import os
import re

# 全局变量存储浏览器驱动实例，防止被垃圾回收
browser_drivers = []

def random_sleep(min_seconds=0.5, max_seconds=2.0):
    """随机睡眠一段时间，模拟人类行为"""
    time.sleep(random.uniform(min_seconds, max_seconds))

# 不再使用人类模拟输入方法
# def human_like_typing(element, text):
#     """模拟人类输入，有随机间隔"""
#     for char in text:
#         element.send_keys(char)
#         # 随机短暂停顿，模拟人类打字速度
#         time.sleep(random.uniform(0.05, 0.25))

def auto_fill_phone(phone_number):
    """
    自动打开SiliconFlow登录页面并填写手机号
    
    参数:
        phone_number (str): 要填写的手机号码
    """
    global browser_drivers
    
    print(f"开始为手机号 {phone_number} 自动填写表单...")
    
    # 创建一个临时目录作为用户数据目录，每次使用不同的目录以隔离会话
    user_data_dir = f"chrome_user_data_{phone_number}"
    
    # 确保目录存在
    os.makedirs(user_data_dir, exist_ok=True)
    
    try:
        # 使用undetected_chromedriver而不是标准selenium
        options = uc.ChromeOptions()
        
        # 添加随机用户代理
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.143 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.143 Safari/537.36 Edg/120.0.0.0"
        ]
        options.add_argument(f"user-agent={random.choice(user_agents)}")
        
        # 设置用户数据目录
        options.add_argument(f"--user-data-dir={os.path.abspath(user_data_dir)}")
        
        # 设置首次运行参数，避免显示首次运行对话框
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        
        # 增加随机性，避免指纹追踪
        options.add_argument(f"--window-size={random.randint(1000, 1920)},{random.randint(700, 1080)}")
        
        # 增加会话隐私性
        options.add_argument("--incognito")
        
        # 禁用自动化扩展
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # 初始化undetected_chromedriver，强制使用与当前Chrome版本兼容的驱动
        driver = uc.Chrome(
            options=options,
            driver_executable_path=None,
            headless=False,
            version_main=133,  # 固定使用Chrome 133版本的驱动
            use_subprocess=True,  # 使用子进程运行，提高稳定性
        )
        
        # 将驱动实例添加到全局列表中，防止被垃圾回收
        browser_drivers.append(driver)
        
        # 设置隐式等待
        driver.implicitly_wait(10)
        
        # 打开登录页面
        url = "https://account.siliconflow.cn/zh/login?redirect=https%3A%2F%2Fcloud.siliconflow.cn%2F%3F"
        driver.get(url)
        print(f"已为手机号 {phone_number} 打开登录页面")
        
        # 随机延迟，模拟人类阅读页面
        random_sleep(1.0, 2.0)
        
        # 尝试找到并填写手机号输入框
        try:
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
                print("未找到手机号输入框，尝试查看页面源码...")
                print(driver.page_source)
                return
            
            # 直接点击输入框
            phone_input.click()
            
            # 清空输入框
            phone_input.clear()
            
            # 直接输入手机号，不再模拟人类输入
            phone_input.send_keys(phone_number)
            
            print(f"已成功填写手机号: {phone_number}")
            
            # 可能的后续操作，如按下Tab键或点击获取验证码
            if random.choice([True, False]):
                action = ActionChains(driver)
                action.send_keys(Keys.TAB).perform()
            else:
                # 尝试查找并点击验证码按钮，但不强制
                try:
                    code_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), '验证码') or contains(text(), '获取')]")
                    if code_buttons:
                        # 鼠标移动到按钮
                        action = ActionChains(driver)
                        action.move_to_element(code_buttons[0]).perform()
                except:
                    pass
            
        except Exception as e:
            print(f"填写手机号时出错: {e}")
            
            # 如果上面的方法失败，可以尝试打印页面源代码帮助调试
            print("页面源代码:")
            print(driver.page_source)
            
    except Exception as e:
        print(f"浏览器操作出错: {e}")
        
    print(f"手机号 {phone_number} 脚本执行完毕")
    # 注意：不要在这里调用driver.quit()，保持浏览器打开

def open_multiple_browsers(phone_numbers):
    """
    同时打开多个浏览器实例并填写不同的手机号
    
    参数:
        phone_numbers (list): 要填写的手机号列表
    """
    threads = []
    
    # 为每个手机号创建一个线程
    for phone in phone_numbers:
        thread = threading.Thread(target=auto_fill_phone, args=(phone,))
        thread.daemon = False  # 设置为非守护线程
        threads.append(thread)
    
    # 启动所有线程
    for thread in threads:
        thread.start()
        # 每个浏览器启动间隔随机延迟，更像人类行为
        random_sleep(2.0, 3.0)
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    print("所有浏览器实例已启动并填写完毕")

def extract_phone_numbers(text):
    """
    从提供的文本中提取手机号
    
    参数:
        text (str): 包含手机号的文本
        
    返回:
        list: 提取到的手机号列表
    """
    phone_numbers = []
    
    # 输出原始文本以便调试
    print("\n原始输入文本:")
    print("-" * 50)
    print(text)
    print("-" * 50)
    
    # 预处理：规范化输入文本
    # 替换多个空格为单个空格
    normalized_text = re.sub(r'\s+', ' ', text)
    # 添加行号便于调试
    lines = normalized_text.split('\n')
    print("\n处理后的文本:")
    for i, line in enumerate(lines):
        print(f"行 {i+1}: {line}")
    
    # 方法1：基本的11位手机号正则表达式
    for number in re.findall(r'1[3-9]\d{9}', text):
        phone_numbers.append(number)
        print(f"方法1找到: {number}")
    
    # 方法2：表格数据处理 - 直接尝试查找特定位置的值
    for line in lines:
        if not line.strip():  # 跳过空行
            continue
            
        # 处理表格行 - 预期格式类似：1 87264 +86 中国广电 北京 19260187144
        parts = re.split(r'\t|\s{2,}|\s+', line.strip())
        
        # 输出分割后的部分，帮助调试
        print(f"分割结果: {parts}")
        
        # 查找可能的手机号
        for part in parts:
            if re.match(r'^1[3-9]\d{9}$', part):
                phone_numbers.append(part)
                print(f"方法2找到: {part}")
    
    # 方法3：专门处理特定格式 - 根据固定位置提取
    for line in lines:
        if not line.strip():  # 跳过空行
            continue
            
        # 针对类似 "1 87264 +86 中国广电 北京 19260187144" 的格式
        # 尝试查找位于第6个位置的11位数字
        parts = re.split(r'\t|\s{2,}|\s+', line.strip())
        if len(parts) >= 6:  # 确保有足够的字段
            potential_phone = parts[5].strip()  # 可能是第6个位置（索引5）
            if re.match(r'^1[3-9]\d{9}$', potential_phone):
                phone_numbers.append(potential_phone)
                print(f"方法3找到(第6位置): {potential_phone}")
    
    # 方法4：直接从特定格式中提取 - 使用更具体的正则表达式
    pattern = r'中国(?:电信|移动|联通|广电)\s+.*?\s+(1[3-9]\d{9})'
    for match in re.findall(pattern, text):
        phone_numbers.append(match)
        print(f"方法4找到: {match}")
    
    # 方法5：使用更宽松的解析，直接查找可能的手机号列
    for line in lines:
        # 查找可能的手机号模式：数字+空格+数字+空格+"+86"+空格+文本+空格+文本+空格+11位数字
        match = re.search(r'\d+\s+\d+\s+\+\d+\s+[\u4e00-\u9fa5]+\s+.*?\s+(1[3-9]\d{9})', line)
        if match:
            phone_numbers.append(match.group(1))
            print(f"方法5找到: {match.group(1)}")
    
    # 去重
    unique_phone_numbers = list(set(phone_numbers))
    
    # 按照11位手机号进行过滤，确保结果都是有效的手机号
    valid_phone_numbers = [
        phone for phone in unique_phone_numbers 
        if re.match(r'^1[3-9]\d{9}$', phone)
    ]
    
    print(f"\n找到 {len(valid_phone_numbers)} 个手机号: {valid_phone_numbers}")
    
    # 如果没有找到任何手机号，尝试最后的方法：直接搜索任何11位数字
    if not valid_phone_numbers:
        print("未找到标准手机号，尝试查找任何11位数字...")
        for number in re.findall(r'\b\d{11}\b', text):
            if number.startswith('1'):
                valid_phone_numbers.append(number)
                print(f"备用方法找到: {number}")
    
    return valid_phone_numbers

if __name__ == "__main__":
    print("手机号批量填写工具")
    print("请粘贴包含手机号的文本，程序将自动提取并打开浏览器填写：")
    print("(输入完成后按两次回车确认)")
    
    # 收集用户输入直到遇到空行
    lines = []
    while True:
        line = input()
        if not line:  # 如果是空行
            break
        lines.append(line)
    
    # 将所有行合并为一个文本
    input_text = "\n".join(lines)
    
    # 从文本中提取手机号
    phone_numbers = extract_phone_numbers(input_text)
    
    # 检查是否找到手机号
    if not phone_numbers:
        print("未在输入文本中找到有效的手机号！")
        exit(1)
    
    # 显示找到的手机号
    print(f"\n成功提取到 {len(phone_numbers)} 个手机号:")
    for i, phone in enumerate(phone_numbers):
        print(f"{i+1}. {phone}")
    
    # 询问用户是否继续
    confirm = input("\n是否使用这些手机号启动浏览器? (y/n): ")
    if confirm.lower() != 'y':
        print("已取消操作。")
        exit(0)
    
    # 直接运行，不再进行确认
    print(f"\n正在启动 {len(phone_numbers)} 个浏览器并填写手机号...")
    open_multiple_browsers(phone_numbers)
    
    # 重要：保持脚本运行，防止浏览器关闭
    print("\n所有操作已完成。浏览器将保持打开状态。")
    print("请按Ctrl+C手动终止此脚本（当您使用完浏览器后）...")
    
    # 无限循环保持脚本运行
    try:
        while True:
            time.sleep(1000)
    except KeyboardInterrupt:
        print("\n脚本已终止，感谢使用！") 