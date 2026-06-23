![](https://ruufly.github.io/medias/keepopen.png)

# KeepOpen

[个人网站](https://ruufly.github.io/) | [Github 仓库](https://github.com/ruufly/KeepOpen) | [开源许可证](https://github.com/ruufly/KeepOpen/blob/main/LICENSE) | [发行版下载](https://github.com/ruufly/KeepOpen/releases)

> 一款保持移动硬盘开启状态的小工具

## 作者

以下列出了参与本项目的作者。

- [@distjr_/@ruufly!](https://github.com/ruufly)

## 使用说明

本工具打开后，自动最小化至系统托盘。通过系统托盘可进入设置页面

设置页面上方可勾选需要保持开启状态的盘符，中间可设置盘符开启状态的刷新时间、是否开机自启动、是否以管理员模式启动等。其中，如需对系统盘使用KeepOpen，建议打开“以管理员模式启动”选项。下方可清理软件运行中的缓存、日志文件等。

## 注意事项

本工具通过修改注册表以实现开机自启动，在一些系统中，卸载后可能无法及时清理注册表残余，请使用`Geek Uninstaller`等工具卸载，或在卸载后手动清理`HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run\`中的残余。
