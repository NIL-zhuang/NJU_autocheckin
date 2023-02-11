# NJU_checkin 🦠

南京大学健康打卡自动形式主义魔法对抗打卡脚本

## 功能描述

1. ⏰ 每日自动进行健康打卡，核酸时间设置为当日或昨日的8-16点
2. 💊 本项目包含Github Actions keep alive模块，可自动激活Github Actions
3. 📧 支持消息推送到pushplus平台
   * action 的消息推送略有延迟，实际使用不影响

## 使用方法

* ❗️在fork本项目并完成配置后，请启动workflow并检查是否已经成功完成签到
* 具体图文步骤参考 [GLaDOS自动签到](https://github.com/NIL-zhuang/GLaDOS_Auto_Checkin)

### 1. 添加 CASTGC 到 Secrets

#### Deprecated web抓包coockie有效期仅1天

1. ~~登陆进[南京大学统一认证](https://authserver.nju.edu.cn/authserver/index.do)网站，使用F12打开开发者工具~~
2. ~~刷新网页，在开发者控制台的 `Application` -> `Storage` -> `Cookies` -> `https://authserver.nju.edu.cn`处，找到CASTGC所对应的Value~~
![CASTGC](https://lemonzzy.oss-cn-hangzhou.aliyuncs.com/typora/202210122147400.png)
3. 在项目页面，依次点击`settings` -> `Secrets` -> `Actions` -> `New repository secret`，建立名为`CASTGC`的secret，值为第二步复制的内容，点击`Add secret`完成添加

#### 获取Android端不过期cookie

1. 登陆进[南京大学统一认证](https://authserver.nju.edu.cn/authserver/index.do)网站，使用F12打开开发者工具
2. 设置安卓客户端User Agent代理，在`开发者工具` -> `More tools` -> `Network conditions`中，取消勾选`Use browser default`，在下方的custom选项中填写对应安卓端UA `Dalvik/2.1.0 (Linux; U; Android 12; 22011211C Build/SP1A.210812.016)`
   ![CASTGC](https://lemonzzy.oss-cn-hangzhou.aliyuncs.com/typora/202210161413004.png)
3. 刷新页面，可以看到整体UI变成了客户端的形式。我们就可以在开发者选项中的`Application` -> `Storage` -> `Cookies`找到`CASTGC`以及对应的Value，一个以TGT开头cas结尾的字符串。
   ![CASTGC](https://lemonzzy.oss-cn-hangzhou.aliyuncs.com/typora/202210161416331.png)
4. 在项目页面，依次点击`settings` -> `Secrets` -> `Actions` -> `New repository secret`，建立名为`CASTGC`的secret，值为`CASTGC`的对应value，点击`Add secret`完成添加

### 2. 添加PUSHPLUS_TOKEN 到 Secrets，不需要推送可以跳过此节

1. 进入[pushplus](http://www.pushplus.plus/)，微信登录账号，在`发送消息` -> `一对一消息`中找到 **你的token**
2. 建立名为`PUSHPLUS_TOKEN`的secret，值为`pushplus`平台token

### 3. 启用Actions

在项目界面，依次点击`Actions` -> `NJU Unhealth Autocheckin` -> `Run workflow` -> `Run workflow`以激活Actions
