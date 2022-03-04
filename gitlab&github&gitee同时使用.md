##### 生成新的SSH keys
###### 生成ssh key介绍
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
###### 如何生成ssh key
```
github

ssh-keygen -t rsa -f ~/.ssh/id_rsa.github -C "youremail@qq.com"


gitee

ssh-keygen -t rsa -f ~/.ssh/id_rsa.gitee -C "youremail@163.com"
```
直接回车3下，就是默认没有密码

###### 秘钥生成完毕
```
Your identification has been saved in id_rsa_gitee.
Your public key has been saved in id_rsa_gitee.pub.
The key fingerprint is:
SHA256:F0K/ojCbFzgMPru11m4g/9uV03oHK+U0rKBLwOOye2c xxx@xxx.com
The key's randomart image is:
+---[RSA 2048]----+
|        .        |
|       . .       |
|  .     . o      |
| . + .   . o     |
|  o X . S o.     |
|  .+.O o.o o*    |
|  oo=o+. .+=.+   |
|   =++E. .oo+ .  |
|  ++.*=o. .o .   |
+----[SHA256]-----+
```
##### 在github/gitlab添加ssh key
###### 复制公钥内容
```
cd ~/.ssh
# 查看 id_rsa_gitee.pub 文件内容
cat id_rsa_gitee.pub

ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDZbvgUEj3XAXH4HkW27ibdXgV6VHdrA9/WdSDHtiiC55mjPvxj3OtPxIbpeJmhWyHiJWR6
uUuK+gkb//O51uWCPhHqxKR7+45tZ9jHqXW+hEKPp+odQgc+3hiHAjTkn3JGeIJlQp2UdJCDHBrp+kcgVeg91+y7cU3ufaUQ/hpD
rCgn6uvwjwJgnDhV9DYi+gFUFe7LUwa1o4nfwg43ycuOOuT7c6VO2dj/0pLRUVTPQYu/C3kaaPVedir7mKIu/dM6Ec44bhYTp1Dq
qp8BO42Cfo+n+dempqYTe2wcPvuDjSj884IATc/KvBfc86Yd2Uj7NI7li90Y3i6adoxUIWQh xxx@xxx.com
```

##### 配置及测试
###### 创建配置文件
在 .ssh 文件夹中创建 config 文件，添加以下内容以区分多个 ssh key：
```
# gitee
Host gitee.com
HostName gitee.com
PreferredAuthentications publickey
IdentityFile ~/.ssh/id_rsa_gitee

# github
Host github.com
HostName github.com
PreferredAuthentications publickey
IdentityFile ~/.ssh/id_rsa_github

#gitlab
Host 47.xxx.xxx.22x
HostName 47.xxx.xxx.xx4
User git
IdentityFile ~/.ssh/id_rsa.gitlab
```
添加完上面的配置后到 github 和 gitlab/ gitee网站添加 ssh。一般位置在账号设置→SSH key
###### 测试是否成功
每个托管商的仓库都有唯一的后缀，比如 Github 的是 git@github.com

至此电脑端配置完毕，将两个ssh分别添加到github和gitee中，测试:

ssh -T git@github.com

ssh -T git@gitee.com

Welcome to Gitee.com, xxxx yourname! //返回这句说明连接正常

##### git常用设置
###### 设置git提交的作者
```
// 查看公共配置
git config --global --list //查看你之前是否设置

//添加公共配置
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"

//删除公共配置
git config --global --unset user.name "你的名字"
git config --global --unset user.email "你的邮箱"

// 查看当前仓库配置
git config --list //查看你之前是否设置

//添加当前仓库配置
git config user.name "你的名字"
git config user.email "你的邮箱"

//删除当前仓库配置
git config --unset user.name "你的名字"
git config --unset user.email "你的邮箱"
```
###### 设置git同时提交github/gitlab
