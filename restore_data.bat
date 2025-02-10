@echo off
REM 检查是否提供了备份目录参数
if "%1"=="" (
    echo 请指定备份目录名称
    echo 用法: restore_data.bat backup_目录名
    exit /b 1
)

set BACKUP_DIR=%1

REM 检查备份目录是否存在
if not exist %BACKUP_DIR% (
    echo 备份目录 %BACKUP_DIR% 不存在
    exit /b 1
)

REM 恢复数据库
if exist %BACKUP_DIR%\app.db (
    copy %BACKUP_DIR%\app.db .\
    echo 数据库已恢复
)

REM 恢复上传文件
if exist %BACKUP_DIR%\uploads (
    xcopy /E /I /Y %BACKUP_DIR%\uploads uploads
    echo 上传文件已恢复
)

REM 恢复临时文件
if exist %BACKUP_DIR%\temp (
    xcopy /E /I /Y %BACKUP_DIR%\temp temp
    echo 临时文件已恢复
)

REM 恢复配置文件
if exist %BACKUP_DIR%\config.py (
    copy %BACKUP_DIR%\config.py .\
    echo 配置文件已恢复
)

echo 恢复完成
pause 