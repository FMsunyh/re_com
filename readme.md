## 相似图检索
### 接口描述
该请求用于实时检索相似图片集合。即对于输入的一张图片（可正常解码，且长宽比适宜），返回自建图库中相似的图片集合。
## 检索
### HTTP 方法：POST
请求URL(测试地址)：http://192.168.38.252:11127/image_retrieval/search

Body中放置请求参数，参数详情如下：
### 请求参数
| 参数	| 是否可选	|类型	|说明|
|-------|---------------- | -------------|-------------|
|image_address  |  是         | string |图片的URL地址|
|Base64_code	|  是	      |string| 图像数据，base64编码，要求base64编码后大小不超过4M，最短边至少15px，最长边最大4096px,支持jpg/png/jpeg格式.|

### 请求代码示例
数据：(二选一)

base64_code:

 ![1](http://192.168.15.214:82/Image/image_retriveal/blob/master/development/server/static/images/github/1.png)

图片地址
 ![2](http://192.168.15.214:82/Image/image_retriveal/blob/master/development/server/static/images/github/2.png)

Curl 发送数据:
 ![3](http://192.168.15.214:82/Image/image_retriveal/blob/master/development/server/static/images/github/3.png)
 
## 返回说明
### 返回参数
|参数	|是否必选	|类型	|说明|
|-------|---------------- | -------------|-------------|
|data	|是	|object[]	|结果数组|
|+index	|是	|string	|图像地址|

返回示例

 ![4](http://192.168.15.214:82/Image/image_retriveal/blob/a514fd283b40e3d9ddd637af20280b873d1cf3e3/development/server/static/images/github/4.png)
 
 
## 安装FLASK-CAS
 
```bash
$ pwd
/usr/local/image_retrieval/development/Flask-CAS
$ sudo chmod -R 777 /usr/local/image_retrieval/development/Flask-CAS
$ python setup.py install
```


## 安装 Elasticsearch-5.2.0
下载 Elasticsearch：
https://www.elastic.co/downloads/past-releases#
 
```bash
$ unzip elasticsearch-5.2.0.zip
$ sudo cp -r elasticsearch-5.2.0 /usr/local/
$ sudo chown -R hadoop:hadoop /usr/local/elasticsearch-5.2.0
$ /usr/local/bin/elasticsearch
```

## 安装 kibana-5.2.0
下载 kibana：
https://www.elastic.co/downloads/past-releases#
 
```bash
$ tar zvxf kibana-5.2.0-linux-x86_64.tar.gz
$ sudo cp -r kibana-5.2.0-linux-x86_64 /usr/local/kibana-5.2.0
$ sudo chown -R hadoop:hadoop /usr/local/elasticsearch-5.2.0
$ cd /usr/local/kibana-5.2.0
$ sudo chown -R hadoop:hadoop /usr/local/kibana-5.2.0/
$ ./bin/kibana
```

 
## 安装maven
下载maven：
http://maven.apache.org/download.cgi
 
```bash
$ tar xzvf apache-maven-3.5.2-bin.tar.gz
$ mv apache-maven-3.5.2 /usr/local/maven-3.5.2
$ export PATH=/usr/local/maven-3.5.2/bin:$PATH
$ mvn --version
Maven home: /usr/local/maven-3.5.2
Java version: 1.8.0_65, vendor: Oracle Corporation
Java home: /opt/modules/jdk1.8.0_65/jre
Default locale: en_US, platform encoding: UTF-8
OS name: "linux", version: "2.6.32-642.el6.x86_64", arch: "amd64", family: "unix"

```

## 导入数据 
* 将图片特征数据导入ES中


## 集群配置
* 集群机器
    * 172.31.100.195
    * 172.31.100.169
* 配置文件：
/usr/local/elasticsearch/config/elasticsearch.yml
* 磁盘：
169用 "/data1/elasticsearch"
195用 "/data11/elasticsearch"
* 集群名和节点名
	* #cluster.name: data-bg-com-ai
	* #node.name: “node-195“
    * 集群名：唯一，所有节点用同一个
* 是否参与master选举和是否存储数据
	* #node.master: true 
	* #node.data: true
* master选举
	* #discovery.zen.minimum_master_nodes: 2
	1. master结点主要用于元数据(metadata)的处理，比如索引的新增、删除、分片分配等。
    2. data 节点上保存了数据分片。它负责数据相关操作，比如分片的 CRUD，以及搜索和整合操作。这些操作都比较消耗 CPU、内存和 I/O 资源
    3. master选举最少的节点数，这个一定要设置为N/2+1，其中N是：具有master资格的节点的数量，而不是整个集群节点个数
* 分片数和副本数
	* #index.number_of_shards: 5 	#index.number_of_replicas: 1

* 新增一个节点
    * cluster.name: data-bg-com-ai
    * node.name: ${HOSTNAME}
    * path.data: /dataXXX/elasticsearch (这里根据host选择磁盘)
    * path.logs: /var/log/elasticsearch
    * network.host: ${HOSTNAME}
    * discovery.zen.ping.multicast.enabled: false
    * discovery.zen.ping.unicast.hosts: ["data5.bg.com", "slave1"]
