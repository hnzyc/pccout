!pip install selenium
!apt-get update
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
!apt-get install google-chrome-stable

# 导入模块

from selenium import webdriver

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By

import time

# 定义目标网址

url = 'https://pccz.court.gov.cn/pcajxxw/index/xxwsy'

# 创建Options对象

options = Options()

# 添加参数

options.add_argument("--headless")

options.add_argument("--no-sandbox")

options.add_argument("--disable-dev-shm-usage")


# 创建Chrome浏览器对象

driver = webdriver.Chrome(options=options)

  

# 打开目标网址

driver.get(url)

  

# 等待网页加载完成

time.sleep(5)

  

# 找到搜索框元素

search_box = driver.find_element(By.XPATH, '//*[@id="search"]')

  

# 输入关键词"信托"

search_box.send_keys('信托机构')

  

# 找到搜索按钮元素

search_button = driver.find_element(By.CSS_SELECTOR, '#qzss_search')


# 点击搜索按钮

driver.execute_script("arguments[0].click();", search_button)

# 点击搜索按钮，click方法无效

# search_button.click()
  
# 等待新的网页打开

time.sleep(5)
  
# 切换到新的窗口句柄

driver.switch_to.window(driver.window_handles[-1])
  

# 获取当前网址

current_url = driver.current_url

# 打印当前网址
# print(current_url)

# 找到搜索结果列表元素

result_list = driver.find_elements(By.CSS_SELECTOR, "#gjsslb > li > div > div > a")
  

# 根据实际情况，定义base_url

base_url = 'https://pccz.court.gov.cn/pcajxxw/pcgg/ggxq?id='

# 遍历所有<a>标签的元素

for element in result_list:

    # 获取onclick属性的值

    onclick_value = element.get_attribute('onclick')

    # 提取onclick属性值中的字符串参数

    string = onclick_value.split("'")[3]

    # 获取标题的内容

    title = element.text

    # 拼接到基础的url中

    url = base_url + string

    # 打印url

    print(title,url)
