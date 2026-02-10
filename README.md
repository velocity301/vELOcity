# E6-2c Ginestra Boot and Operating Instructions
### EUT Ethernet I/O Cable Legend
- **Net MGT Port:** <span style="color:orange">Orange</span> Tab.
- **Serial MGT Port:** <span style="color:#FFDD00">Yellow</span> Tab

### Step 0: Open a window for Ping
RoT port will not be connected for this test
```cmd
ping -t -s 1 -w 2000 10.129.31.41
```

### Step 1: Serial Port
#### For Performance Criteria A Tests
Start the COM Serial window in MobaXterm for E6-2c at speed 115200
This will be window#1
```Serial
username: sunservice
password: changeme
cd /persist/Compliance; ./status_mii_tool
```
confirm Net MGT port reported by the above command is linked at the correct speed and duplex for this test;
otherwise change ethernet switch to TRENDNET switch
Do not proceed until correct

### Step 2: Booting and Net MGMT for /HOST/console
Open a new MobaXterm window
This will be window#2
```sp
ssh root@10.129.31.41
password: changeme
->start /SYS
->start /HOST/console
username: root
password: linux1
/opt/snbench/snbench -m probe
```
<br>

>[!WARNING]
>The above takes a few to several minutes to finish running.  just be patient.
>after it is eventually finished running, always perform the following check before moving on: ensure the above >command output the following at the end: 
>
>```host/console
>The Device:# Pensando appears to have linked correctly.
>```
>Later, you may run /root/Compliance/enumerate_Pensando.sh to verify the links.
>If one or more ortano does not math the above for every pensando card, contact zain and rodney.
>If one or more ortano does not train at the expected speed and link width, testing will be invalid, so ensure it is correct before continuing.

Next, enter the command to start the internal USB Ethernet: 
```host/console
/root/Compliance/Internal_USB_Ethernet_bringup.sh
```
MAKE SURE THE ABOVE ENDS BY PRINTING OUT THE FOLLOWING TWO LINES
```host/console
ens_usb_int: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
    inet 169.254.182.77  netmask 255.255.255.0  broadcast 169.254.182.255
```
<br>

>[!WARNING]
>PAY PARTICULAR ATTENTION TO THE HOST'S inet ADDRESS ABOVE AT 169.254.182.77.  IF THIS IS NOT SHOWN, CONTACT RODNEY, AND DO NOT START TESTING UNTIL RESOLVED.

Finally for this window, enter the following command
```host/console
while true; do hostname | awk -F'.' '{printf "%s timestamp: ",$1 }'; date; sleep 1; done
```
\
NOTES FOR SHUTDOWN WHEN YOU ARE READY TO MOVE TO A NEW TEST STATION...
This tab in MobaXterm window#2 will be what you use to shutdown the system. 
to stop the continuous command above, press **\<CTRL+C>**
Then enter the command: 
```host/console
shutdown -h now
```
**wait for the output**
```host/console
Started Power-Off.
Reached target Power-Off.
mlx5_core 0000:f1:00.1: Shutdown was called
			mlx5_core 0000:f1:00.0: Shutdown was called
			mlx5_core 0000:11:00.1: Shutdown was called
			mlx5_core 0000:11:00.0: Shutdown was called
			ACPI: PM: Preparing to enter system sleep state S5
reboot: Power down
```
Wait until you can see the last line before exiting the /HOST/console using the key combination **ESC -> (**
Now that you've returned to the SP, you can ensure that the system is powered off with the following command:
```sp
->show /SYS
```
look for a line that says: 
```sp
power_state = Off
```
Do not remove power to the system before confirming this

<!-- ### Step 3: RoT Exerciser
Not present for this system -->

### Step 3: Three tasks to periodically run on the SP
Open MobaXterm window#3 and ssh into sunservice
```sunservice
ssh sunservice@10.129.31.41
password: changeme
```
enter the following command into sunservice:
```sunservice
cd /persist/Compliance
./check_system_info ; mii-tool eth0 ; echo ; hostname | awk -F'.' '{printf "%s timestamp: ",$1}'; date ; echo
```

CHECK THAT THE "/persist/Compliance/check_system_info" SHOWS THE FOLLOWING:
```sunservice
"The state of 'hwdiag si' matches the reference file at"
```
IF THE "/persist/Compliance/check_system_info" OUTPUTS THE FOLLOWING:
```sunservice
"ERROR!!!  The output of 'hwdiag si' now does not match the reference file!"
```
THEN USE MOBAXTERM WINDOW#2 TO REBOOT
NEXT, CHECK THAT THE SP NET MGMT "eth0: negotiated" TO THE CORRECT SPEED AND DUPLEX AND "flow-control, link ok".

Next, do all of the fault management check, both before, during, and after testing:
```sunservice
fmadm faulty -e; fmdump -eiv -t 2026-02-09/12:30:00; echo; hostname | awk -F'.' '{printf "%s timestamp: ",$1}'; date ; echo
```
You can modify the "2026-02-09/12:30:00" portion of the string as you see fit to help with pruning the list, but...
only after you have checked and are sure everything was okay from the last AC power cycle of the rack to the new data and time you want to substitute
>[!WARNING]
>IF ANY SUSPICIOUS OR UNKNOWN REPORTS ARE LISTED, CONTACT THE COMPLIANCE ENGINEER AND RODNEY.

Next, run the following command: 
```sunservice
./svcio_uptime.sh
```

This tells you how long the service I/O on the RoT has been alive.  it should be a reasonable number based on the last time the SP/RoT were intentionally power cycled or rebooted.
If it seems like the svcio may have rebooted during a test, notify the compliance engineer and/or Rodney

### Step 4: Run SunVTS
Open MobaXterm window#4. Within this window:
```host
ssh root@10.129.31.42
password: linux1
cd /usr/sunvts/bin
./startsunvts -t
```
Go to Session, List, down and then right arrow to select "EMC", Press Enter to select it, and then Load it
Wait for the "Session_Name: EMC" to appear in the lower left corner.
Highlight Start and hit Enter to run.
After testing is over, record each subsystem's Passes and Errors (as appropriate for the Perf. Criterion level required by the test where Perf. A must be zero errors), and wait for VTS to increment passes.

### Step 5: Exercise second Mellanox port
Open MobaXterm window#5. Enter the following command:
```host
ssh root@10.129.31.43
password: linux1
ping 169.254.182.76
```
The same private internal IP for the SP is always used on every system. If the system is not pinging correctly, contact Rodney as there must have been a problem in step #2.

### Step 6: Periodically Check for PCIE errors on each of the nodes
Open MobaXterm window#6. 
```host
ssh root@10.129.31.42
password: linux1
cd /root/Compliance/PCIe_Fabric_Error_Reporter/
./PCIe_Fabric_Error_Reporter.sh
```
Periodically check manually for any errors.
If there is one or more UE, the test has failed.
If there are CE which are continually occurring (you will have to run the command a second time to see if there are more ce this time than when you ran it ~30 seconds ago), then the test has failed.

### Step 7: Check Mellanox cards' link status
Open MobaXterm window#7. 
```host
ssh root@10.129.31.42
password: linux1
cd /root/Compliance
./show_network_link_status.sh
```
Make sure the number of lines shown match the number of Mellanox ports (there are two ports per card) installed in the system.
Make sure the "link detected:" are all listed as "yes".
Make sure the speed is correct for each of the card types.
Make sure the duplex is "full" for all links on all nodes.
rerun and check this periodically before, during, and after testing.

---

If there is any question at all, call Rodney.
