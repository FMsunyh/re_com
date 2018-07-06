# 商品识别
## 服务安装部署
###  Conda 安装说明
确保机器安装了Annaconda. 参考地址：https://www.anaconda.com/
### python环境安装
进入development目录，执行install.sh
```bash
cd  '.../commdity_recognition/development'
bash install.sh
```

### 开启服务
```bash
cd  '.../commdity_recognition/development'
bash worker.sh
```

### 重启服务
```bash
cd  '.../commdity_recognition/development'
bash reboot_worker.sh
```

### 杀死服务
```bash
cd  '.../commdity_recognition/development'
bash kill_worker.sh
```