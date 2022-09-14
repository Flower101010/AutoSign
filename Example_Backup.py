def punchCard(id,paw,email):
    try:
       	#获取chrome驱动，启动浏览器并进入打卡页面
        Option=webdriver.ChromeOptions()
        Option.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=Option)
        #driver = webdriver.Chrome()
        driver.get("https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0")
        time.sleep(1)
        # 输入账号
        driver.find_element(By.XPATH,'''//*[@id="mt_5"]/div[2]/div[3]/input''').send_keys(id)
        # 输入密码
        driver.find_element(By.XPATH,'''//*[@id="mt_5"]/div[3]/div[3]/input''').send_keys(paw)
        # 点击登录按钮
        driver.find_element(By.XPATH,'''//*[@id="mt_5"]/div[5]/div/input''').click()
        time.sleep(3)
        # 进入填报页面
        driver.switch_to.frame('zzj_top_6s')  #千万不要删除！！！
        driver.find_element(By.XPATH,'''//*[@id="bak_0"]/div[11]/div[3]/div[4]/span''').click()
        time.sleep(5)
        # 提交填报
        driver.find_element(By.XPATH,'''//*[@id="btn416a"]/span''').click()
        time.sleep(1)
        # 返回提交信息
        fanhui = driver.find_element(By.XPATH,'''//*[@id="bak_0"]/div[2]/div[2]/div[2]/div[2]''').text
        print("填报成功！") 
        # 发送填报成功邮件
        subject = "打卡返回信息"
        content = "打卡信息! \n "+fanhui
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
