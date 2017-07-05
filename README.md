# alertmt
Simple python script to check directories and send email alerts with Message Type and TRN
Script consists 2 configuration files ([YAML format](https://en.wikipedia.org/wiki/YAML)):
1) alertsmtp.yml – mail server configuration – I don’t know your parameters, maybe it is needed to review.
2) alert.yml – scan configuration, more detailed description further.

alert.yml
each configuration block begins with ‘---‘ from 1-th position. Here one block:
```YAML
---
# directory to scan. NOTE: '\' at the end mandatory!
cur_path: 'c:\work\alert\out\'
# file mask to scan 
cur_mask: '*.out'
# new folder to move files. NOTE: '\' at the end mandatory!
new_dir: 'c:\work\alert\out2\'
# new extension to rename files
new_ext: 'out'
# message type to scan
mtyp: 103
# substring to find with message type
ftag: '{2:O103'
# to get TRN from message text
trnf: ':20:'
# list of the receiver to inform
rcvr: [bash@alliance.ru, support@alliance.ru]
# email subject, TRN will be added at the end
em_subj: MTXXX was received
# email text
em_text: email text block 001
```
You can add several blocks to inform about O103 or O202, or I103, I202 and so on.
Receiver list can be present in one string:
```YAML
rcvr: [bash@alliance.ru, support@alliance.ru]
```
or each email on separate line with ‘-‘ at the beginning, indention also mandatory:
```YAML
rcvr:
    - bash@alliance.ru
    - support@alliance.ru
```
I have 3 ideas to avoid sending notification several times:
1) Create list of processed files – not good, it can be very long. Tail from time to time also bad, sophisticated logic
2) Check time – very sophisticated logic because there are several times (creation, modification, last opening), these parameters have different cense in Unix and Windows, you remember. We obtain files from Unix – also time drift between systems is possible… to sum it up, very complicated and unreliable.
3) Read file and rename/move from input stream (folder). So we have guarantee that we will not send notification twice and we will avoid gaps in the input stream. Simple logic, fast and reliable.

How it works:
- Script scans files by ‘cur_mask’ in folder ‘cur_path’
- When found substring ‘ftag’ file will be moved/renamed according to ‘new_dir’ / ‘new_ext’, you can just move files to new folder, or just rename or together.
- Read TRN from message, create email and send it to receivers in list ‘rcvr’

Important to understand the logic: script checks files in the folders BUT not the REAL message flow
- alert.py – python script, created on python 3.4.1
- alert.yml – scan configuration
- alertsmtp.yml – SMTP server config file. It is needed to test or maybe make some changes because it will depend from your SMTP server.

One more important thing:
I did not catch any exceptions – existing of configuration files, folders, and so on.
Be careful to use.
