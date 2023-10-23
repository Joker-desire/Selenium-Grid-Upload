# Selenium Grid Upload

**Selenium Grid 模拟操作上传操作问题解决方案**

> 在使用Selenium Grid模拟操作上传文件时，会从浏览器实例的本地文件系统中读取文件。这就导致了一个问题，如果Grid
> Hub所在的机器上没有要上传的文件，那么就会出现文件不存在的错误。

## 解决

将浏览器实例的某一文件夹映射出来，在执行上传操作时，将文件上传到该文件夹中，这样就可以解决文件不存在的问题。

### 步骤

1. 在每个浏览器镜像中，创建一个文件夹，例如：`/home/seluser/upload`
   ```yml
   volumes:
      - ./upload:/home/upload
   ```
2. 在执行上传时中，将文件上传到该文件夹（`./upload`）中, 在代码中就可以使用`/home/upload`来访问该文件夹下的文件了
   ```python
   ele = driver.find_element(By.XPATH, "//input[@type='file']")
   ele.send_keys("/home/upload/xxx.txt")
   ```

## 增强处理

***提供上传接口，可以在执行上传文件模拟操作之前，先使用接口进行上传***

1. 起一个fastapi服务，提供上传接口
2. 将服务中的upload文件夹映射到`./upload`文件夹中,实现文件共享
3. 将所有服务使用NGINX进行代理

### 说明

1. Selenium Grid ui界面
   ```text
   http://127.0.0.1:8080/ui
   ```

2. Selenium Grid Hub
   ```text
   http://127.0.0.1:8080/grid/hub
   ```

   ```python
   from selenium import webdriver
   from selenium.webdriver.chrome import options
   
   # from selenium.webdriver.firefox import options
   # from selenium.webdriver.edge import options
   
   driver = webdriver.Remote(command_executor="http://admin:admin@127.0.0.1:8080/grid/hub", options=options.Options())
   ```

3. Selenium Grid 状态
   ```text
   http://127.0.0.1:8080/grid/hub/status
   ```

4. 上传接口

   ```text
   http://127.0.0.1:8080/api/upload
   ```
   ```python
   import requests
   
   
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

   
   files_path = upload(["/Users/example/Pictures/6.JPG", "/Users/example/Pictures/7.png"])
   print(files_path)
   
   # ['/home/upload/2023/10/22/19676048770179.JPG', '/home/upload/2023/10/22/19676121458637.png']
   ```

## 部署启动（[Selenium-Grid-Upload](https://github.com/Joker-desire/Selenium-Grid-Upload)）

### 部署

1. 克隆项目
   ```bash
   git clone https://github.com/Joker-desire/Selenium-Grid-Upload.git
   ```
2. 进入项目目录
    ```bash
    cd Selenium-Grid-Upload
   ```
3. 运行
    ```bash
    sh grid.sh run
   ```
4. 默认superuser
    ```text
    username: admin
    password: admin
   ```

### 命令行

1. 运行
   ```bash
   sh grid.sh run

   # 指定启动多少个浏览器实例
   sh grid.sh run --scale chrome=5 --scale edge=1 --scale firefox=5
   ```
2. 启动
   ```bash
   sh grid.sh start
   ```
3. 重启
   ```bash
   sh grid.sh restart
   ```
4. 停止
   ```bash
   sh grid.sh stop
   ```
5. 删除
   ```bash
   sh grid.sh down
   ```
6. 创建新的superuser
    ```bash
    sh grid.sh superuser <username>
    ```

## 示例

```python
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

```