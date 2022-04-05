from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import base64
import json
import requests
from PIL import Image
import time

option = webdriver.ChromeOptions()
# option.add_argument('--headless')
driver = webdriver.Chrome(options=option)


# 打码平台api
def base64_api(uname, pwd, img, typeid):
    with open(img, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]


# 鼠标轨迹复原函数（防坐标叠加）
def click_locxy(dr, x, y, left_click=True):
    """
    dr:浏览器
    x:页面x坐标
    y:页面y坐标
    left_click:True为鼠标左键点击，否则为右键点击
    """
    if left_click:
        ActionChains(dr).move_by_offset(x, y).click().perform()
    else:
        ActionChains(dr).move_by_offset(x, y).context_click().perform()
    ActionChains(dr).move_by_offset(-x, -y).perform()  # 将鼠标位置恢复到移动前


def usual(rank):
    # 验证码左 上 右 下坐标
    location = (300, 240, 630, 650)
    # 获取全屏截图
    driver.get_screenshot_as_file('full_page.png')
    # 打开全屏截图 截取验证码并保存
    page_pic = Image.open('full_page.png')
    yzm_pic = page_pic.crop(location)
    yzm_pic.save('yzm_pic.png')
    # 定位验证码
    result = base64_api(uname='chank', pwd='cx413616', img="./yzm_pic.png", typeid=22)
    print(result)
    # 分离并模拟点击
    for i in result.split("|"):
        j = i.split(",")
        click_locxy(driver, 300 + int(j[0]), 240 + int(j[1]))
        time.sleep(1)
    # 验证码确定 5s
    if rank == 1:
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[6]/div/div/div[3]/a/div").click()
    else:
        driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[6]/div/div/div[3]/a/div").click()
    time.sleep(5)
    if rank == 1:
        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[4]/div[2]/ul/li[3]/a")
            return 0
        except:
            usual(1)
    else:
        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[1]/ul/li[1]/span")
            return 0
        except:
            usual(0)


# 进入米游社首页 10s
driver.get("https://bbs.mihoyo.com/ys/")
time.sleep(10)
# 打开登录页面 3s
driver.find_element(By.XPATH,
                    "/html/body/div[1]/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/button").click()
time.sleep(3)
# 选择密码登录 1s
driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[4]/div/div[2]/div[1]/div/div[2]/span").click()
time.sleep(1)
# 输入账号密码 1s 注：此处可以更改账号密码
driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[4]/div/div[2]/form/div[1]/div/input").send_keys(
    "13525250615")
time.sleep(1)
driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[4]/div/div[2]/form/div[2]/div/input").send_keys("cx413616")
# 获取验证码 5s
driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[4]/div/div[2]/form/div[4]/button").click()
time.sleep(5)
# 执行通用验证码坐标点击函数
usual(1)

# 再次进入账号管理中心 10s
driver.execute_script('window.open("https://user.mihoyo.com/#/login/password");')
time.sleep(10)
# 标签句柄切换
driver.switch_to.window(driver.window_handles[1])
# 输入账号密码 1s
driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/form/div[1]/div/input").send_keys(
    "13525250615")
time.sleep(1)
driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/form/div[2]/div/input").send_keys("cx413616")
# 获取验证码 5s
driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/form/div[4]/button").click()
time.sleep(5)
# 执行通用验证码坐标点击函数
usual(0)

cookies = driver.execute_script("return document.cookie;")
qq_config = {
    "enable_Config": True,
    "config_Version": 4,
    "mihoyobbs_Login_ticket": "",
    "mihoyobbs_Stuid": "",
    "mihoyobbs_Stoken": "",
    "mihoyobbs_Cookies": "",
    "mihoyobbs": {
        "bbs_Global": True,
        "bbs_Signin": True,
        "bbs_Signin_multi": True,
        "bbs_Signin_multi_list": [2, 5],
        "bbs_Read_posts": True,
        "bbs_Like_posts": True,
        "bbs_Unlike": True,
        "bbs_Share": True
    },
    "genshin_Auto_sign": True,
    "honkai3rd_Auto_sign": False
}
with open(f"../mihoyo/config/2351686624.json", "w") as temp_flie4:
    qq_config["mihoyobbs_Cookies"] = cookies
    json.dump(qq_config, temp_flie4, sort_keys=False, indent=4, separators=(', ', ': '),
              ensure_ascii=False)
