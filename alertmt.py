#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import glob
import yaml
import smtplib
from email.mime.text import MIMEText

# load email configuration
mailcfg = yaml.load(open('alertsmtp.yml'))
print(mailcfg)
# load scan configuration
config_all = yaml.load_all(open('alert.yml'))
for config in config_all :
    print(config)                                                           
# for each entity in scan configuration
for config in config_all :             
# scan files                                                                   
    for file_name in glob.glob(config['cur_path'] + config['cur_mask']) :                               
# read message from file
        ms_text = open(file_name, 'r').read()                                                            
# tag to find e.g '{2:O103'
        if (ms_text.find(config['ftag']) > 0) :                                                         
# rename and/or move files according to config
            os.rename(file_name, config['new_dir'] + os.path.basename(file_name).split('.')[0] + '.' + config['new_ext'])
            ms_trnf_pos = ms_text.find(config['trnf']) + len(config['trnf'])                             
# get TRN (f20) from text
            ms_trnf = ms_text[ms_trnf_pos:].split('\n')[0]                                              
# add message type and TRN into email subject
            em_subj = config['em_subj'].replace('XXX', str(config['mtyp'])) + ' TRN: ' + ms_trnf        
# send emails to recepients according to config
            s = smtplib.SMTP(mailcfg['smtp'], mailcfg['port'])                                           
            s.set_debuglevel(mailcfg['debuglevel'])
            if mailcfg['auth'] == 'yes' :
                s.login(mailcfg['username'], mailcfg['password'])
            if mailcfg['starttls'] == 'yes' :
                s.starttls()
            msg = MIMEText(config['em_text'])
            msg['Subject'] = em_subj
            msg['From'] = mailcfg['sender']
            msg['To'] = ", ".join(config['rcvr']) 
            s.sendmail(mailcfg['sender'], config['rcvr'], msg.as_string())                              
# show status
            print(em_subj)
            s.quit()            
