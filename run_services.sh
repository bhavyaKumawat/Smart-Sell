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
