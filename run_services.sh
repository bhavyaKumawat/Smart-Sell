#!/bin/bash
nohup python3 -m ss_ingest > ./log/ss_ingest.log &
nohup python3 -m lb_user_svc > ./log/lb_user_svc.log &
nohup python3 -m lb_processor_svc > ./log/lb_processor_svc.log &
nohup python3 -m lookup_svc > ./log/lookup_svc.log &
nohup python3 -m ss_archive_svc > ./log/ss_archive_svc.log &
