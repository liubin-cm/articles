rem ���е�������
rem 1. ��������������.net 4.0������
rem 2. ��ȷ������nugetԴ
rem 3. ���securitydev�����д���
rem 4. 

@echo off
echo %~dp0
rem CUR_DIR��ʾ���������ڵ�Ŀ¼��������·���ָ���\
set CUR_DIR=%~dp0
cd /d %~dp0
cd ..
rem PAR_DIR��ʾ���������ڵ�Ŀ¼�ĸ�Ŀ¼��������·���ָ���\
set PAR_DIR=%cd%

rem TARGET����Ŀ�꣬��������ȫ���¹���ReBuild��Ҳ��������������Build
set TARGET=%1

set MSBUILD=%windir%\Microsoft.NET\Framework\v4.0.30319\MSBuild.exe
%MSBUILD% /t:%TARGET% %CUR_DIR%\build.targes