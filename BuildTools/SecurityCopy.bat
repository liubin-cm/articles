rem ���е�������
rem 1. ��������������.net 4.0������
rem 2. ��ȷ������nugetԴ
rem 3. ���iddev�����д���
rem 4. ����Bk.Core.Imp.csproj��GameIdUI.csproj��FastDFS.Client�汾��DLLĿ¼�а汾��һ�£���Ҫ�ֶ��޸�FastDFS.ClientӦ�ã��ñ༭���򿪣������ļ������ּ���
rem 5. GameIdUI.csproj��AdminMainIdUi.csproj��GameIdUILayer�����ޱ仯��GameIdUILayer�������벻ͨ�����޸�������DLLĿ¼�е�DLL

@echo off
echo %~dp0
rem CUR_DIR��ʾ���������ڵ�Ŀ¼��������·���ָ���\
set CUR_DIR=%~dp0
cd /d %~dp0
cd ..
rem PAR_DIR��ʾ���������ڵ�Ŀ¼�ĸ�Ŀ¼��������·���ָ���\
set PAR_DIR=%cd%
set /P dest=������Ŀ��·��(��󲻴�\)��

rem TARGET����Ŀ�꣬��������ȫ���¹���ReBuild��Ҳ��������������Build
set TARGET=Copy

set MSBUILD=%windir%\Microsoft.NET\Framework\v4.0.30319\MSBuild.exe
%MSBUILD% /t:%TARGET% /p:DestDir=%dest%\ %CUR_DIR%\build.targes