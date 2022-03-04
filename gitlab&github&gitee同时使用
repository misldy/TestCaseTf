##### 清除之前的git全局配置
###### 之前安装过git且配置过邮箱和用户名的执行下面语句删除之前的git配置:
```
git config --global --list //查看你之前是否设置

//删除之前的配置
git config --global --unset user.name "你的名字" //删除之前的名字配置
git config --global --unset user.email "你的邮箱"//删除之前的名字配置
```
##### 生成新的SSH keys
如前所述，许多 Git 服务器(包括但不限于gitee、github、gitlab)都使用 SSH 公钥进行认证。 为了向 Git 服务器提供 SSH 公钥，如果某系统用户尚未拥有密钥，必须事先为其生成一份。 这个过程在所有操作系统上都是相似的。 首先，你需要确认自己是否已经拥有密钥。 默认情况下，用户的 SSH 密钥存储在其 ~/.ssh 目录下。 进入该目录并列出其中内容，你便可以快速确认自己是否已拥有密钥：
```
$ cd ~/.ssh
$ ls
authorized_keys2  id_dsa       known_hosts
config            id_dsa.pub
# 生成 key，将邮件地址替换为你 Gitee 或者 Github 使用的邮件地址
$ ssh-keygen -t rsa -C "xxx@xxx.com"
```
密钥文件夹目录(C:\Users\username\.ssh),之前没有创建过的为空

​我们需要寻找一对以 id_dsa 或 id_rsa 命名的文件，其中一个带有 .pub 扩展名。 .pub 文件是你的公钥，另一个则是与之对应的私钥。

如果找不到这样的文件（或者根本没有 .ssh 目录），你可以通过运行 ssh-keygen 程序来创建它们。 在 Linux/macOS 系统中，ssh-keygen 随 SSH 软件包提供；在 Windows 上，该程序包含于 MSysGit 软件包中。