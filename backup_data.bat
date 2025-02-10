@echo off
REM 创建备份目录
set BACKUP_DIR=backup_%date:~0,4%%date:~5,2%%date:~8,2%
mkdir %BACKUP_DIR%

REM 备份数据库
if exist app.db (
    copy app.db %BACKUP_DIR%\
    echo 数据库已备份
)

REM 备份上传文件
if exist uploads (
    xcopy /E /I uploads %BACKUP_DIR%\uploads
    echo 上传文件已备份
)

REM 备份临时文件
if exist temp (
    xcopy /E /I temp %BACKUP_DIR%\temp
    echo 临时文件已备份
)

REM 备份配置文件
if exist config.py (
    copy config.py %BACKUP_DIR%\
    echo 配置文件已备份
)

echo 备份完成，文件保存在 %BACKUP_DIR% 目录中
pause 