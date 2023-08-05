import asyncio
from pyppeteer import launch
import time

async def get_webpage_content_with_headless_browser(url, headers, css_selector):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.setExtraHTTPHeaders(headers) # 设置请求头
    await page.goto(url)
    

     # 执行点击操作
    await page.click("#layui-layer1 > div.layui-layer-btn > a")
    await asyncio.sleep(2)
    await page.click("body > div.middleDiv.ixm > div.mainDiv.has-nav > div.left > span")
    await asyncio.sleep(2)
    await page.click("body > div.middleDiv.ixm > div.mainDiv.has-nav > div.left.active > ul > li.PermitApplication")
    await asyncio.sleep(14)

    await page.click("body > div.middleDiv.ixm > div.mainDiv.has-nav > div.mainContent > div > div.basic-panel-body.textAlignCenter.page.pageShow > div > div.driverRow > div.row-button.bg-org > div.row-button-click > a.application-btn.able")
    await asyncio.sleep(7)

    await page.click("#permitApplication-page > div.subpage.pageShow > p.bold.marginTop10 > div")
    await asyncio.sleep(2)
    await page.click("#permitBtnNext")
    await asyncio.sleep(7)

    await page.click("#licenseApplyForm > ul > li:nth-child(1) > dl > dt")
    await asyncio.sleep(2)


    try:
        await page.waitForSelector(css_selector)
        content = await page.evaluate(f'document.querySelector("{css_selector}").textContent')
    except Exception as e:
        print("Error occurred while fetching the webpage:", e)
        content = None

    await browser.close()
    return content

def monitor_webpage(url,  headers, css_selector, interval=300):

    previous_content = None

    while True:

        current_content = asyncio.get_event_loop().run_until_complete(get_webpage_content_with_headless_browser(url,headers, css_selector))

        if previous_content is None:
            previous_content = current_content

        if current_content != previous_content:
            print("Content has changed!")
            print("Previous content:", previous_content)
            print("Current content:", current_content)
        else:
            print("Content has not changed")

        previous_content = current_content

        time.sleep(interval)



if __name__ == "__main__":
    target_url = "http://218.5.80.22:9093/OnlineService/Overview"  # 替换成你想获取元素的网页地址
    css_selector = "#licenseApplyForm > div.examTimeList"   # 替换成你想获取的元素的CSS选择器
    your_cookie_value = "ASP.NET_SessionId=3nlopdmb4nzm0w5cjgn13g1h"
    
    headers = {
    "Cookie": your_cookie_value,}
    monitor_webpage(target_url, headers, css_selector)
