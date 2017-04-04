# 5200K Product Backend Project

## 简介

本项目是5200小程序后台项目，使用 Python Flask 框架。

---

## 安装使用

本项目使用[Python 2.7](https://www.python.org/downloads/), [MongoDB 3.2.7](https://www.mongodb.org/) 版本。

1. 同步代码

    使用git下拉代码。

2. 安装依赖

    建议使用 Python 虚拟环境运行项目，打开虚拟环境后，在项目根目录下运行 `pip install -r requirements.txt` 安装依赖的 python 第三方库。
    如果安装过程中出现错误，尝试安装依赖的系统库 `sudo apt-get install python-dev libffi-dev libssl-dev libxml2 libxml2-dev libxslt-dev`。

3. 设置配置

    在项目根目录的 configs 文件夹下，把 `configs.example.py` 复制至相同目录下的 `__init__.py` 文件
    并修改里面的配置项。每个子模块都有自己独立的配置项，需要在其根目录下把 `config.example.py` 复制至当前目录的 `configs.py` 文件。

4. 运行程序

    在项目根目录下输入 `python server.py` 即可运行程序。若 `config/__init__.py` 里面的 DEBUG 配置项为 True，则程序会检查代码的更新并且自动重启；正式环境中 DEBUG 必须要设置为 False。 
    
5. 项目 wiki

    项目的接口和模型 wiki 全部配置在 `wiki.py` 脚本中，当更新了接口或者模型注释后，需要运行 `python wiki.py` 更新项目 wiki。
    注意：只有拥有项目 master 分支使用权限的用户才能成功的运行 wiki 脚本。

---

## 项目约定

为了保持代码风格的一致和，增加整体项目的可阅读、可维护性，本项目做了一些代码风格和逻辑实现上的约定，希望开发人员在开发时能够遵守这些约定。

1. 所有时间相关的字段使用 UTC datetime 格式储存，返回给前端时没有特殊需求统一转换成 UTC 时间戳返回。

2. API 的注释使用 markdown 格式书写，方便直接用脚本生成项目的 wiki。注释示例如下：

    ```python
    @api.route('/user', methods=['POST'])
    def create_user():
        """
        ## Create User
        More Description of this api.
        
            POST '/api/user'

        Params:
        * `username` (string) - User name
        * `password` (string) - Md5 user password
        * `signature` (string) *optional* - User signature
        
        Returns:
        * `_id` - New user id
        
        Errors: `1001` `1002`
        
        ---
        """
        pass
    ```

3. 项目的 API 设计遵循 restful 风格，可参考 [设计指南](http://www.ruanyifeng.com/blog/2014/05/restful_api.html)

4. 在项目中使用了新的第三方库之后，要将该第三方库以及使用的版本号写入 `requirements.txt` 文件中，建议的使用方式是在虚拟环境中使用 pip 安装，
然后运行 `pip freeze > requirements.txt` 命令更新文件。

5. 项目的错误返回信息包括以下字段 `stat=0`, `err`, `msg`，错误信息定义在模块中的 Error 类中。

6. 数据库表和字段名以及函数和变量名使用 Python 的下划线表示法，API url 单词之间使用短横线(-)隔开。所有常量使用大写，并使用下划线分割。

7. 项目内的重要变量名命名参照[业务术语表](#) （待定）。

---

## 更新历史

* 2017-04-04 第一次更新 by @xgiton