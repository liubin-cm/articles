rem 运行的条件：
rem 1. 本批处理运行在.net 4.0环境下
rem 2. 正确设置了nuget源
rem 3. 检出iddev下所有代码
rem 4. 由于Bk.Core.Imp.csproj和GameIdUI.csproj中FastDFS.Client版本与DLL目录中版本不一致，需要手动修改FastDFS.Client应用，用编辑器打开，保留文件名部分即可
rem 5. GameIdUI.csproj和AdminMainIdUi.csproj中GameIdUILayer长期无变化，GameIdUILayer单独编译不通过，修改其引用DLL目录中的DLL

@echo off
echo %~dp0
rem CUR_DIR表示批处理所在的目录，其后带有路径分隔符\
set CUR_DIR=%~dp0
cd /d %~dp0
cd ..
rem PAR_DIR表示批处理所在的目录的父目录，其后带有路径分隔符\
set PAR_DIR=%cd%
set /P dest=请输入目标路径(最后不带\)：

rem TARGET构建目标，可以是完全重新构建ReBuild，也可以是增量构建Build
set TARGET=Copy

set MSBUILD=%windir%\Microsoft.NET\Framework\v4.0.30319\MSBuild.exe
%MSBUILD% /t:%TARGET% /p:DestDir=%dest%\ %CUR_DIR%\build.targes