#!/usr/bin/env python

import sys
import pathlib
import asyncio
import re

CLI_PARAM_NUMBER = 3
HELP = """Please use the script with parameters as follows:

PortScanner.py hosts_file ports_file
    
where hosts_file - a text file with hostnames(IP adresses)
      ports_file - a text file with ports required to check

Every record in those files must be at the new line"""
    
async def nmap_scan_host(host_name: str, required_ports_to_check: list[int]) -> dict:
    proc = await asyncio.create_subprocess_shell(
        f"nmap {host_name}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()
    result = parse_nmap_result(host_name, stdout.decode())

    if "open_ports" in result.keys(): #if host was successfully scanned then check ports
        for port in required_ports_to_check:
            if port not in result["open_ports"]:
                result["closed_ports"].append(port)

    return result


def parse_nmap_result(host_name: str, nmap_result: str) -> dict:
    host_down_msg = "Host seems down"
    host_resolve_failed_msg = "Failed to resolve"

    if host_down_msg in nmap_result:
        return {"host": host_name, "msg": host_down_msg}
    if host_resolve_failed_msg in nmap_result:
        return {"host": host_name, "msg": host_resolve_failed_msg}
    

    open_ports_regexp = r'[0-9]+\/[a-z]+\s+open' #it will find lines with "80/tcp  open  http" and etc from result
    open_ports_lines = re.findall(open_ports_regexp, nmap_result)

    #convert ports to int value and put them to the list
    open_ports = []
    for port_string in open_ports_lines:
        separator = port_string.find("/")
        open_ports.append(int(port_string[:separator]))  #get value before firts "/"
    
    return {"host": host_name, "open_ports":open_ports, "closed_ports": []}



async def nmap_scan_hosts(hosts: list[str], required_ports_to_check: list[int] = []):
    tasks = []
    async with asyncio.TaskGroup() as tg:
        for host in hosts:
            tasks.append(tg.create_task(nmap_scan_host(host, required_ports_to_check)))
        await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)

    result = []
    for task in tasks:
        result.append(task.result())
    
    print(result)
        

    

if __name__ == "__main__":
    if len(sys.argv) != CLI_PARAM_NUMBER:
        print(HELP)
        quit()
    
    h_file = pathlib.Path(sys.argv[1])
    p_file = pathlib.Path(sys.argv[2])

    if (h_file.is_file() == False):
        print("Couldn't find hosts_file")
        quit()
    if (p_file.is_file() == False):
        print("Couldn't find ports_file")
        quit()

    with h_file.open('r') as f:
        hosts = f.readlines()
    hosts = [host.strip() for host in hosts]
    
    with p_file.open('r') as f:
        ports = f.readlines()
    ports = [int(port) for port in ports]
    

    asyncio.run(nmap_scan_hosts(hosts, ports))


