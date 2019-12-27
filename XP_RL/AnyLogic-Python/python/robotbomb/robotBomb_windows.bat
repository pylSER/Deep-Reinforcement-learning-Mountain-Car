@echo off
rem 
rem Run AnyLogic Experiment
rem 
chcp 1252 >nul 
set DIR_BACKUP_XJAL=%cd%
cd /D "%~dp0"

for /f "delims=" %%a in ('dir "%ProgramFiles%\Java\j*" /o-d /ad /b') do (
	set PATH_XJAL="%ProgramFiles%\Java\%%a\bin\java.exe"
	if exist "%ProgramFiles%\Java\%%a\bin\java.exe" goto exitloop
)
:exitloop

set OPTIONS_XJAL=--illegal-access=deny
if %PROCESSOR_ARCHITECTURE% == x86 set OPTIONS_XJAL=

rem Use the following lines if you run 32-bit java under 64-bit OS
rem set PATH_XJAL="%ProgramFiles(x86)%\Java\jre8\bin\java.exe"
rem set OPTIONS_XJAL=

if not exist %PATH_XJAL% set PATH_XJAL="%JAVA_HOME%\bin\java.exe"
if not exist %PATH_XJAL% set PATH_XJAL=java
echo on
%PATH_XJAL% %OPTIONS_XJAL% -cp model.jar;lib/com.anylogic.engine.jar;lib/com.anylogic.engine.nl.jar;lib/com.anylogic.engine.sa.jar;lib/sa/ioutil-8.3.jar;lib/sa/com.anylogic.engine.sa.web.jar;lib/sa/executor-basic-8.3.jar;lib/sa/spark/slf4j-api-1.7.21.jar;lib/sa/spark/jackson-annotations-2.8.5.jar;lib/sa/spark/jetty-webapp-9.4.8.v20171121.jar;lib/sa/spark/javax.servlet-api-3.1.0.jar;lib/sa/spark/jetty-io-9.4.8.v20171121.jar;lib/sa/spark/jetty-security-9.4.8.v20171121.jar;lib/sa/spark/jackson-datatype-jsr310-2.8.5.jar;lib/sa/spark/jetty-servlet-9.4.8.v20171121.jar;lib/sa/spark/jetty-server-9.4.8.v20171121.jar;lib/sa/spark/websocket-client-9.4.8.v20171121.jar;lib/sa/spark/commons-codec-1.10.jar;lib/sa/spark/jackson-databind-2.8.5.jar;lib/sa/spark/jackson-core-2.8.5.jar;lib/sa/spark/jsch-0.1.54.jar;lib/sa/spark/websocket-common-9.4.8.v20171121.jar;lib/sa/spark/jetty-util-9.4.8.v20171121.jar;lib/sa/spark/spark-core-2.7.2.jar;lib/sa/spark/jetty-client-9.4.8.v20171121.jar;lib/sa/spark/jetty-http-9.4.8.v20171121.jar;lib/sa/spark/jetty-xml-9.4.8.v20171121.jar;lib/sa/spark/websocket-server-9.4.8.v20171121.jar;lib/sa/spark/jetty-servlets-9.4.8.v20171121.jar;lib/sa/spark/websocket-servlet-9.4.8.v20171121.jar;lib/sa/spark/websocket-api-9.4.8.v20171121.jar;lib/sa/util-8.3.jar;lib/database/querydsl/querydsl-core-4.2.1.jar;lib/database/querydsl/querydsl-sql-4.2.1.jar;lib/database/querydsl/querydsl-sql-codegen-4.2.1.jar;lib/database/querydsl/guava-18.0.jar -Xmx512m robotbomb.qUpdate %*
@echo off
if %ERRORLEVEL% neq 0 pause
echo on
@cd /D "%DIR_BACKUP_XJAL%"
