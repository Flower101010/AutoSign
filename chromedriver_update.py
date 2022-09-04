import os
import re
import winreg
import zipfile
import requests

base_url = 'http://npm.taobao.org/mirrors/chromedriver/'
version_re = re.compile(r'^[1-9]\d*\.\d*.\d*')  # 匹配前3位版本号的正则表达式


def getChromeVersion():
    """通过注册表查询chrome版本"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Google\\Chrome\\BLBeacon')
        value, t = winreg.QueryValueEx(key, 'version')
        return version_re.findall(value)[0]  # 返回前3位版本号
    except WindowsError as e:
        # 没有安装chrome浏览器
        return "1.1.1"


def getChromeDriverVersion():
    """查询Chromedriver版本"""
    outstd2 = os.popen('chromedriver --version').read()
    try:
        version = outstd2.split(' ')[1]
        version = ".".join(version.split(".")[:-1])
        return version
    except Exception as e:
        return "0.0.0"

def get_path():
    '''查询系统内Chromedriver的存放路径'''
    outstd1 = os.popen('where chromedriver').read()
    return outstd1.strip('chromedriver.exe\n')


def unzip_driver(path):
    '''解压Chromedriver压缩包到指定目录'''
    f = zipfile.ZipFile("chromedriver.zip",'r')
    for file in f.namelist():
        f.extract(file, path)


def getLatestChromeDriver(version):
    # 获取该chrome版本的最新driver版本号
    url = f"{base_url}LATEST_RELEASE_{version}"
    latest_version = requests.get(url).text
    print(f"与当前chrome匹配的最新chromedriver版本为: {latest_version}")
    # 下载chromedriver
    print("开始下载chromedriver...")
    download_url = f"{base_url}{latest_version}/chromedriver_win32.zip"
    file = requests.get(download_url)
    with open("chromedriver.zip", 'wb') as zip_file:  # 保存文件到脚本所在目录
        zip_file.write(file.content)
    print("下载完成.")
    # 解压
    path = get_path()
    print('解压路径路径为:', path)
    unzip_driver(path)
    print('升级完成')

def checkChromeDriverUpdate():
    chrome_version = getChromeVersion()
    print(f'当前chrome版本: {chrome_version}')
    driver_version = getChromeDriverVersion()
    print(f'当前chromedriver版本: {driver_version}')
    if chrome_version == driver_version:
        print("版本兼容,无需更新.")
        return
    print("chromedriver版本与chrome浏览器不兼容,更新中>>>")
    try:
        getLatestChromeDriver(chrome_version)
        print("chromedriver更新成功!")
    except requests.exceptions.Timeout:
        print("chromedriver下载失败,请检查网络后重试!")
    except Exception as e:
        print(f"chromedriver未知原因更新失败: {e}")


if __name__ == "__main__":
    checkChromeDriverUpdate()