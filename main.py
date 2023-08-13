# 导入模块
import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 定义目标网址
url = 'https://pccz.court.gov.cn/pcajxxw/index/xxwsy'

# 定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

# 发送请求并获取响应
response = requests.get(url, headers=headers)

# 解析响应内容
soup = BeautifulSoup(response.text, 'html.parser')

# 找到搜索框元素
search_box = soup.find('input', id='search')

# 修改搜索框元素的value属性为'信托机构'
search_box['value'] = '信托机构'

# 找到搜索按钮元素
search_button = soup.find('input', id='qzss_search')

# 修改搜索按钮元素的onclick属性为'javascript:;'
search_button['onclick'] = 'javascript:;'

# 将修改后的搜索框元素和搜索按钮元素重新插入到soup对象中
search_box.insert_after(search_button)

# 将soup对象转换为字符串
html = str(soup)

# 定义一个函数，用于模拟浏览器执行JavaScript代码，并返回执行结果
def execute_script(script, html):
    # 导入模块
    import execjs
    
    # 创建一个JavaScript运行环境
    context = execjs.compile("""
        function execute(script, html) {
            // 创建一个虚拟的DOM对象
            var document = {};
            
            // 定义document对象的write方法，用于接收html字符串
            document.write = function(html) {
                this.html = html;
            };
            
            // 定义document对象的querySelector方法，用于根据CSS选择器查找元素
            document.querySelector = function(selector) {
                // 导入模块
                var cheerio = require("cheerio");
                
                // 加载html字符串，创建一个cheerio对象
                var $ = cheerio.load(this.html);
                
                // 根据CSS选择器查找元素，并返回第一个匹配的元素
                return $(selector)[0];
            };
            
            // 执行传入的JavaScript代码
            eval(script);
            
            // 返回修改后的html字符串
            return this.html;
        }
    """)
    
    # 调用execute函数，并传入JavaScript代码和html字符串，返回执行结果
    return context.call("execute", script, html)

# 调用execute_script函数，传入搜索按钮元素的onclick属性值和html字符串，返回执行结果
html = execute_script(search_button['onclick'], html)

# 重新解析执行结果
soup = BeautifulSoup(html, 'html.parser')

# 找到搜索结果列表元素
result_list = soup.select('#gjsslb > li > div > div > a')

# 根据实际情况，定义base_url
base_url = 'https://pccz.court.gov.cn/pcajxxw/pcgg/ggxq?id='

# 创建一个空列表，用于存放爬取结果
results = []

# 遍历所有<a>标签的元素
for element in result_list:
    # 获取onclick属性的值
    onclick_value = element['onclick']
    
    # 提取onclick属性值中的字符串参数
    string = onclick_value.split("'")[3]
    
    # 获取标题的内容
    title = element.text
    
    # 拼接到基础的url中
    url = base_url + string
    
    # 将标题和url组成一个元组，添加到结果列表中
    results.append((title, url))

# 定义一个函数，用于发送邮件
def send_email(results):
    # 定义邮件内容，使用HTML格式
    content = '<h1>爬虫结果</h1><ul>'
    for title, url in results:
        content += f'<li><a href="{url}">{title}</a></li>'
    content += '</ul>'
    
    # 创建MIMEText对象，指定内容、格式和编码
    message = MIMEText(content, 'html', 'utf-8')
    
    # 定义邮件主题
    subject = '爬虫结果'
    
    # 设置邮件主题
    message['Subject'] = Header(subject, 'utf-8')
    
    # 定义发件人邮箱账号和密码，从环境变量中获取
    sender = 'crawler@utrust.cn'
    password = os.environ.get('EMAIL_PASSWORD')
    
    # 定义收件人邮箱账号，可以是多个
    receivers = ['zhaoyunchao@utrust.cn', 'liji@utrust.cn']
    
    # 创建SMTP对象，指定服务器地址和端口
    smtp = smtplib.SMTP_SSL('smtp.utrust.cn', 465)
    
    # 登录发件人邮箱账号和密码
    smtp.login(sender, password)
    
    # 发送邮件，指定发件人、收件人和邮件内容
    smtp.sendmail(sender, receivers, message.as_string())
    
    # 关闭SMTP对象
    smtp.quit()

# 调用send_email函数，传入爬取结果，发送邮件
send_email(results)
