import requests
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.common.by import By


def upload(pictures):
    """
    上传图片
    :param pictures: 图片路径列表
    :return: 图片上传后在浏览器实例中的路径列表
    """
    url = "http://admin:admin@127.0.0.1:8080/api/upload"
    files = [("files", open(picture, 'rb')) for picture in pictures]
    response = requests.post(url, files=files)
    if response.status_code == 401:
        raise Exception("Authorization Required")
    elif response.status_code != 200:
        raise Exception("Upload Failed")
    else:
        res = response.json()
        return [data.get("browser_file_path") for data in res.get("data", [])]


# 在需要执行上传的模拟程序前，先进行上传需要用到的图片
files_path = upload(["/Users/example/Pictures/6.JPG", "/Users/example/Pictures/7.png"])

driver = webdriver.Remote(command_executor="http://admin:admin@127.0.0.1:8080/grid/hub", options=options.Options())

driver.get("https://www.example.com/upload.html")

ele = driver.find_element(By.XPATH, "//input[@type='file']")
for file_path in files_path:
    # 通过上传后的图片获取浏览器中的路径进行上传
    ele.send_keys(file_path)

driver.quit()
