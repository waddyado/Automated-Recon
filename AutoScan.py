import subprocess
import time
import os
import threading



resultfilename = 'scan_results.txt'
iisfilename = 'iis_servers.txt'
scan_data = []
IIS_servers = []
IIS_exists = False

finished_number = 0


def gather_domains():
        
        target = str(input('Enter Target to Scan:>'))
        print(f'[*]TARGETING {target}')
        print('[-]Enumerating domains')
        time.sleep(20)
        result = subprocess.check_output(['subfinder', '-d', f'{target}', '-o', 'output.txt'])
        #print(result)
        print('[*] Domains Gathered... Starting Scan Procedure')
        thread_scans()



def thread_scans():
        global finished_number
        
        #select intensity
        while True:
                intensity = input('What intensity do you want to scan with(1-3):>')
                try:
                        int(intensity)
                        if int(intensity) < 1:
                                print('Please enter an integer from the range 1-3')
                        elif int(intensity) > 3:
                                 print('Please enter an integer from the range 1-3')
                        else:
                                intensity = int(intensity)
                                if intensity == 1:
                                        print(f'[-]Intensity set to Light')
                                elif intensity == 2:
                                        print(f'[-]Intensity set to Medium')
                                elif intensity == 3:
                                        print(f'[-]Intensity set to Heavy') 
                                break
                
                except:
                        print('Please enter an integer from the range 1-3')

        while True: #open file and create threads
                file = ('output.txt')
                count = 1
                linecount = 0
                
                with open(str(file), 'r') as f: #count lines in file
                        for line in f:
                                linecount +=1
                time.sleep(1)
                f.close()
                print(f'\n[*] Scanning {linecount} hosts')
                with open(str(file), 'r') as f:
                        for line in f: #read every line from file and nmap scan content from every line
                                time.sleep(1)
                                target = line.strip() #remove whitespace
                                print(f'\n[*]Scanning host {line}\n')
                                
                                t1 = threading.Thread(target=scan, args=(target, intensity))
                                t1.start()
                break

        waitcount = 0
        while True: #wait for threads to finish
                if finished_number == linecount:
                        break
                if waitcount > 20: #wait one minute for threads to finish. If not, continues anyway
                        break
                else:
                        print(f'[*] Waiting for threads to complete {finished_number}/{linecount}')
                        time.sleep(3)
                        waitcount += 1
                        continue
                
                                

def scan(target, intensity):
                global finished_number
                global IIS_exists
                                
                if intensity == 1:
                        scan = subprocess.check_output(['nmap', str(target)])#simple scan
                elif intensity == 2:
                        scan = subprocess.check_output(['nmap', '-sV', '-T4', '-O', '-F', '--version-light', str(target)])#quick scan plus
                elif intensity == 3:
                        scan = subprocess.check_output(['nmap', '-T4', '-A', '-v', str(target)])#intense scan
                                
                scan_result = bytes.decode(scan)#decode output from bytes
                                
                if '0 hosts up' in scan_result:
                        print('\n[*]Host is not responding')#if host is down
                                        
                else:
                        if 'Microsoft IIS' in scan_result:#if running IIS, append to list
                                print('[*]Server is runnng IIS')
                                IIS_exists = True
                                IIS_servers.append(str(target))
                        scan_data.append(scan_result)#add result to list
                        #print(scan_data)
                                        
                
                print('\n[*]Scan Complete')
                finished_number += 1
        
        
gather_domains()

results = open(resultfilename, 'w')#write scan data to file
for i in range(0, len(scan_data)):
               print(f'writing index {i} to file')
               results.write(scan_data[i] + '\n')
print(f'done writing to {resultfilename}')
results.close()

if IIS_exists == True:#write servers running IIS to file if any exist
        iisresults = open(iisfilename, 'w')
        print(IIS_servers)
        for i in range(0, len(IIS_servers)):
                       print(f'writing index {i} to file')
                       iisresults.write(IIS_servers[i] + '\n')
        print(f'done writing to {iisfilename}')                  
        iisresults.close()

print('\n[*] Script Finished. Happy Hunting :D')

