@echo off
chcp 936 > nul
setlocal

git rev-parse --is-inside-work-tree > nul 2>&1
if not errorlevel 1 goto stage
echo 错误：当前目录不是 Git 仓库，无法提交和推送。
exit /b 1

:stage
git add .
if not errorlevel 1 goto diff
echo 错误：暂存改动失败。
exit /b 1

:diff
git diff --cached --quiet
if errorlevel 1 goto commit
echo 没有需要提交的改动。
goto push

:commit
git commit -m "update"
if not errorlevel 1 goto push
echo 错误：提交改动失败。
exit /b 1

:push
git push
if not errorlevel 1 goto success
echo 错误：推送到远程仓库失败。
exit /b 1

:success
echo 已成功提交改动，GitHub Actions 正在自动构建上线！
endlocal
