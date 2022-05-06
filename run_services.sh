#!/bin/bash
export host_name=""
export port_no=9000
nohup python3 -m ss_ingest > ./log/ss_ingest.log &
export host_name=""
export port_no=9001
nohup python3 -m lb_user_svc > ./log/lb_user_svc.log &
nohup python3 -m lb_processor_svc > ./log/lb_processor_svc.log &
nohup python3 -m lookup_svc > ./log/lookup_svc.log &
nohup python3 -m ss_archive_svc > ./log/ss_archive_svc.log &
export host_name=""
export port_no=9002
nohup python3 -m utils_svc > ./log/utils_svc.log &
export host_name=""
export port_no=9003
nohup python3 -m file_svc > ./log/file_svc.log &
export host_name=""
export port_no=9004
nohup python3 -m email_svc > ./log/email_svc.log &
export host_name=""
export port_no=9005
nohup python3 -m lookup_svc_retro > ./log/lookup_svc_retro.log &
export host_name=""
export port_no=9006
nohup python3 -m ss_archive_svc_retro > ./log/ss_archive_svc_retro.log &
