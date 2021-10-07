# NirsSystem
NIRS API instantiated system constructed based on auto-nirs system, it can instantiate the relevant API into a direct use of Web system







使用docker部署启动

```bash
# 容器启动
$ sudo docker-compose up
# 容器重新编译后启动
$ sudo docker-compose up --build
# 容器启动(精灵线程)
$ sudo docker-compose up -d --build
# 查询容器状态
$ sudo docker-compose ps
# 确认本地打开的tcp端口号
$ netstat -nltp
# Web访问测试
$ curl http://127.0.0.1:8081
# 执行myweb容器内的命令
$ sudo docker-compose run myweb top
# 查看容器输出日志
$ sudo docker-compose logs -f
# 容器停止
$ sudo docker-compose stop
# 容器停止+消除(容器+网络)
$ sudo docker-compose down
# 容器停止+消除(容器+网络+镜像)
$ sudo docker-compose down --rmi all
```

