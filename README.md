# 免费代理IP爬虫 & IP有效性校验

## 代理IP爬取

爬取三一代理、西刺代理和无忧代理三个网站上的免费代理IP信息，并持久化到MySQL，表结构如下所示：

```mysql
CREATE TABLE `proxy_ip_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `proxy_ip` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5085 DEFAULT CHARSET=utf8mb4;
```

## IP有效性校验

*注：由于免费IP大概率无法使用，或者存活时间较短；且IP爬取的速率远高于IP校验，所以不建议在爬取信息的同时进行有效性校验。*

### 校验思路

挂代理访问待爬取的目标网站URL即可

### 实现方式

通过并发 + 定时轮询，实现高效且持续的校验 [详见源码](https://github.com/YHYR/ProxyIpSpider/tree/master/ProxyIpSpider/script)

