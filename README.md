# PortScanner

This is a very simple Python script in order to scan ports for specified hosts via `nmap` CLI tool. It also uses asyncio to scan ports in parallel.

# Usage

`PortScanner.py hosts_file ports_file`

- hosts_file - a text file with hostnames(IP adresses)
- ports_file - a text file with ports required to check

Every record in those files must be at the new line

# Example
**Input:**

`./PortScanner.py hosts.txt ports.txt`

- hosts.txt:  
`192.168.0.104`   
`192.168.0.100`  
`192.168.0.103`

- hosts.txt:  
`80`  
`99`  
`127`  
`443`

**Output:**  

`[{'host': '192.168.0.104', 'msg': 'Host seems down'}, {'host': '192.168.0.100', 'open_ports': [8008, 8009, 8443, 9000], 'closed_ports': [80, 99, 127, 443]}, {'host': '192.168.0.103', 'open_ports': [], 'closed_ports': [80, 99, 127, 443]}]`

