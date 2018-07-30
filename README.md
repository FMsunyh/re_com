# 商品识别
## 商品识别服务安装部署
###  Conda 安装说明
确保机器安装了Annaconda. 参考地址：https://www.anaconda.com/
### 运行环境安装
进入development目录，执行install.sh
```bash
cd  '.../commdity_recognition/development/'
bash install.sh
```

### 模型权重
将模型权重存放在目录：".../commdity_recognition/development/server/weights/" 下.
权重文件名：rel_weight.h5

### 开启服务
```bash
cd  '.../commdity_recognition/development/'
bash worker.sh
```

### 测试服务
执行测试文件test_server.py
```python
cd  '.../commdity_recognition/development/'
python test_server.py -ip 192.168.1.210

```
**192.168.1.210 服务部署的主机ip地址**


如果看到以下输出，说明服务已经正常启动，以下为输出样例：
```json
{
  "status": 100000,
  "data": [
    "glg-glgblzbg-hz-mcxcw-45g,0.931,1049,570,1492,1103",
    "bl-blht-dz-yw-6.7g,0.850,493,516,1121,1148",
    "bl-blht-dz-yw-6.7g,0.850,493,516,1121,1148",
    "wwsp-wwxxs-dz-yw-60g,0.838,660,253,1248,591",
    "wwsp-wwxxs-dz-yw-60g,0.838,660,253,1248,591",
    "wwsp-wwxxs-dz-yw-60g,0.838,660,253,1248,591"
  ],
  "msg": "success"
}
```

### 重启服务
```bash
cd  '.../commdity_recognition/development/'
bash reboot_worker.sh
```

### 杀死服务
```bash
cd  '.../commdity_recognition/development/'
bash kill_worker.sh
```

商品识别服务部署说明文件
编写：孙永海
时间：2018年7月9日
