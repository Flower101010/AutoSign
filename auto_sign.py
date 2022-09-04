from selenium import webdriver
import time
from selenium.webdriver.common.by import By

#引入模块
import chromedriver_update 
import mail
import Identify_image

#以下打卡函数仅为示例，需要根据打卡网站进行调整！！！
def punchCard(id,paw,email):
    # 打卡
    try:
       	#获取chrome驱动，启动浏览器并进入打卡页面
        Option=webdriver.ChromeOptions()
        Option.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=Option)
        #driver = webdriver.Chrome()
        driver.get("你的打卡网址")
        time.sleep(1)
        # 输入账号
        driver.find_element(By.XPATH,'''输入账号的XPATH路径''').send_keys(id)
        # 输入密码
        driver.find_element(By.XPATH,'''输入账号的XPATH路径''').send_keys(paw)
        # 点击登录按钮
        driver.find_element(By.XPATH,'''点击的XPATH路径''').click()
        time.sleep(3)
        # 进入填报页面
        driver.switch_to.frame('Example_test')  #用于找到Frame，不一定需要
        driver.find_element(By.XPATH,'''进入填报按钮的XPATH''').click()
        time.sleep(1)
        # GetImage
        img = driver.find_element(By.XPATH,'图形验证码的XPATH')
        img.screenshot('pictures.png')
        time.sleep(3)
        # 识别图形验证码
        res= Identify_image.identifye('pictures.png')
        #print(res)
        # 填写验证码
        driver.find_element(By.XPATH,'''验证码填入的XPATH''').send_keys(res)
        time.sleep(1)
        # 提交填报
        driver.find_element(By.XPATH,'''填报按钮的XPATH''').click()
        time.sleep(1)
        # 返回提交信息
        fanhui = driver.find_element(By.XPATH,'''提交信息的XPATH''').text
        print("填报成功！") 
        # 发送填报成功邮件
        subject = "打卡成功"
        content = "恭喜您打卡成功！"+fanhui
        mail.sendEmail(email,subject,content)
    except:
        print("填报失败！")
        # 发送填报失败邮件
        subject = "打卡失败"
        content = "出现错误"
        mail.sendEmail(email,subject,content)

    finally:
        #退出浏览器
        driver.quit()



if __name__ == "__main__":
    try:
        chromedriver_update.checkChromeDriverUpdate()
        punchCard('yourcount','yourpassward','Youremail@example.com')
    except:
        mail.sendEmail('Youremail@example.com','打卡程序出错','出错')
        print('something wrong')

