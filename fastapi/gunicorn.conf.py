import multiprocessing

# 是否开启debug
debug = False

# 绑定ip和端口号
bind = '0.0.0.0:8080'

# 超时时间
timeout = 30

# 工作模式
worker_class = 'uvicorn.workers.UvicornWorker'

# 进程数
workers = multiprocessing.cpu_count() * 2 + 1

# 设置证书
# keyfile = ''
# certfile = ''

# 日志级别，这个日志级别指的是错误日志级别，而访问日志的级别无法设置
loglevel = 'debug'

# 日志配置
accesslog = "/tmp/gunicorn_access.log"
# 错误日志文件
errorlog = "/tmp/gunicorn_error.log"
