rem 运行的条件：
rem 1. 本批处理运行在.net 4.0环境下
rem 2. 正确设置了nuget源
rem 3. 检出securitydev下所有代码
rem 4. 

@echo off
echo %~dp0
rem CUR_DIR表示批处理所在的目录，其后带有路径分隔符\
set CUR_DIR=%~dp0
cd /d %~dp0
cd ..
rem PAR_DIR表示批处理所在的目录的父目录，其后带有路径分隔符\
set PAR_DIR=%cd%

rem TARGET构建目标，可以是完全重新构建ReBuild，也可以是增量构建Build
set TARGET=%1

set MSBUILD=%windir%\Microsoft.NET\Framework\v4.0.30319\MSBuild.exe
%MSBUILD% /t:%TARGET% %CUR_DIR%\build.targes