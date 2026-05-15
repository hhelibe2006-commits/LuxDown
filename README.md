# 🎬 LuxDown – 基于 yt‑dlp 与 PySide6 的视频下载工具

**LuxDown** 是一款跨平台视频下载图形界面工具，底层使用 `yt-dlp`，上层采用 `PySide6` 构建。支持多链接批量解析、选择性下载、实时进度显示，以及下载路径、内容类型、输出格式等灵活配置。


---

## 📜 许可证

本项目使用 **GNU Affero General Public License v3.0 (AGPL-3.0)** 开源协议。  
详细条款请查看 [LICENSE](LICENSE) 文件。

---

## ⚠️ 免责声明

**本软件仅供个人学习与研究使用。**  
用户使用 LuxDown 下载任何内容，均应遵守当地法律法规及目标网站的条款与条件。开发者（hhelibe2006）不对用户通过本软件下载、保存、传播或使用任何内容的行为承担任何法律责任。  
用户需自行判断下载内容的合法性与授权情况。若因不当使用导致任何版权纠纷、法律诉讼或其他后果，均由用户自行承担，与项目开发者无关。  
使用本软件即表示您已阅读并同意本免责声明。

---

## ✨ 功能特点

- **多链接支持** – 同时添加多个视频 / 播放列表链接，批量解析。
- **选择性下载** – 解析后列出所有可下载项，自由勾选需要的视频。
- **实时进度** – 下载过程中显示进度条、速度、已下载大小等。
- **灵活配置**  
  - 📁 自定义下载路径  
  - 🎞️ 选择下载内容（仅视频 / 仅音频 / 视频+音频）  
  - 🧾 选择输出格式（mp4, mkv, webm, mp3, m4a 等）
- **跨平台** – Windows / macOS / Linux 均可运行（源码运行方式）。

---


## 🚀 快速开始（源码运行）

### 环境要求
- Python 3.10 或更高版本
- pip 包管理器

### 1. 克隆仓库
```bash
git clone https://github.com/hhelibe2006-commits/LuxDown.git
cd LuxDown
```

### 2. 安装依赖
推荐使用虚拟环境：

```bash
# 创建虚拟环境（可选）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 安装依赖
pip install .

# 生成多语言文件(unix系统用户使用/)
pyside6-lrelease .\src\*.ts
```

### 3. 运行
```bash
python src/main.py
```

---

## 🏗️ 编译与打包（Windows）

项目使用 **Nuitka** 编译为独立可执行文件，并使用 **NSIS** 制作安装包。

### 环境准备
1. 安装 Python (3.8+)
2. 安装 Nuitka 及依赖：
   ```bash
   pip install nuitka
   ```
3. 安装 **Clang**（用于 `--clang` 参数）或使用 MinGW。确保编译器已加入 PATH。
4. 安装 **NSIS**（用于打包安装程序）。

### 编译命令
在项目根目录下执行：
```bash
nuitka --standalone --show-progress --plugin-enable=pyside6 src\main.py --clang --windows-console-mode=disable --jobs=1 --low-memory --windows-icon-from-ico=.\src\LuxDown.ico --windows-company-name="hhelibe2006" --windows-product-name="LuxDown" --windows-file-version=1.0.0.0 --windows-product-version=1.0.0.0 --windows-file-description="这是一款用于下载视频的软件"
```
执行后会在 `src/main.dist` 或当前目录生成 LuxDown 的独立文件夹。

### 制作 NSIS 安装程序
编写 NSIS 脚本，示例如下
```
# 1. 定义版本和名称常量
!define PRODUCT_NAME "LuxDown"
!define PRODUCT_VERSION "1.0.1"
!define EXE_NAME "main.exe"

# 引入基础逻辑库
!include "MUI2.nsh"
!include "FileFunc.nsh"

RequestExecutionLevel admin

# 2. 设置软件详细信息 (鼠标右键属性可见)
VIProductVersion "${PRODUCT_VERSION}.0"
VIAddVersionKey "ProductName" "${PRODUCT_NAME}"
VIAddVersionKey "Comments" "安装包"
VIAddVersionKey "FileDescription" "视频下载器"
VIAddVersionKey "FileVersion" "${PRODUCT_VERSION}"
VIAddVersionKey "ProductVersion" "${PRODUCT_VERSION}"

Name "${PRODUCT_NAME}"
OutFile "${PRODUCT_NAME}-${PRODUCT_VERSION}.win-x64.exe"
InstallDir "$PROGRAMFILES64\${PRODUCT_NAME}" ; 建议64位系统使用 $PROGRAMFILES64

# --- 界面设置 (可选，让安装包更像样) ---
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "SimpChinese"

Section "Install"
    SetOutPath "$INSTDIR"
    # 释放文件
    File /r "C:\Users\hhhhh\PycharmProjects\LuxDown\main.dist\*.*"

    # 创建快捷方式
    CreateShortcut "$DESKTOP\${PRODUCT_NAME}.lnk" "$INSTDIR\${EXE_NAME}" "" "$INSTDIR\LuxDown.ico" 0

    # 写入卸载程序
    WriteUninstaller "$INSTDIR\Uninstall.exe"

    # --- 注册到控制面板 (卸载列表可见) ---
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" "DisplayName" "${PRODUCT_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" "UninstallString" '"$INSTDIR\Uninstall.exe"'
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" "DisplayIcon" "$INSTDIR\${EXE_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" "DisplayVersion" "${PRODUCT_VERSION}"
SectionEnd

Section "Uninstall"
    # 删除文件
    RMDir /r "$INSTDIR"
    # 删除快捷方式
    Delete "$DESKTOP\${PRODUCT_NAME}.lnk"
    # 删除注册表信息
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
SectionEnd
```
然后鼠标右键生成：
```bash
makensis installer.nsi
```
---
## 📝 使用说明

1. **添加链接** – 向文本框输入链接，每行一个链接。
2. **解析链接** – 点击 “解析”，程序会获取每条链接中的所有视频/音频信息。
3. **选择项目** – 在设置选择你想要下载的条目。
4. **设置选项** – 在设置选择输出路径、下载类型（视频/音频/视频+音频）、格式。
5. **开始下载** – 点击 “下载”，实时进度显示在状态区域。

---

## 🛠️ 技术栈

- **yt-dlp** – 下载核心引擎
- **PySide6** – GUI 框架
- **Nuitka** – Python 编译器
- **NSIS** – 安装包制作工具

---

## 🙏 致谢

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) 项目团队
- Qt for Python 社区
- Nuitka 与 NSIS 开发者

如果这个工具对你有帮助，请给一个 ⭐️ **Star** 支持一下！
