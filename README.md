# CPSC\_471 \- Group_5 File Transfer Protocol Server and Client Applications

**Authors:** Alfredo Llamas, Kyler Farnsworth, Andres Perez, Mustafa Atakan Tan, & Joel Talamayan\.

**Emails:**  
frankllamas@csu\.fullerton\.edu  
KFarnsworth1@csu\.fullerton\.edu  
perez\.andres@csu\.fullerton\.edu  
mtan17@csu\.fullerton\.edu  
jtalamayan@csu\.fullerton\.edu

**Language Used:** Python\.

## How to Start Server and Client Applications
To start the server and client on a comand line interface write the following for server and client\.

### Server:
> **Linux:** python3 send\_file\_server\.py <*PORT\_NUMBER*>

> **Windows:** py send\_file\_server\.py <*PORT\_NUMBER*>

*SERVER\_PORT* is the port at which the server accepts connection request\.

### Client:
> **Linux:** python3 send\_file\_client\.py <*SERVER\_MACHINE*> <*SERVER\_PORT*>

> **Windows:** py send\_file\_client\.py <*SERVER\_MACHINE*> <*SERVER\_PORT*>

*SERVER\_MACHINE* is the domain of the server\.  
*SERVER\_PORT* is the port at which the server accepts connection request\.

## FTP Command Interpreter Instructions
Upon connecting to the server, the client will enter is command interpreter and wait for instructions giving prompt `ftp>` to the user\. The following are commands that are recognized by our FTP\.  

* **_get_** <*REMOTE\_FILE*>  
Downloads file REMOTE_FILE from the server\.

* **_put_** <*LOCAL\_FILE*>  
Uploads file LOCAL_FILE to the server\.

* **_ls_**  
Prints a listing of the contents on the remote server\.

* **_quit_**  
Disconnects from the server and exits\.