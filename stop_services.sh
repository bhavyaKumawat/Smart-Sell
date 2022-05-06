#!/bin/bash
nohup pkill -f ss_ingest > ./log/ss_ingest.log &
nohup pkill -f lb_user_svc > ./log/lb_user_svc.log &
nohup pkill -f lb_processor_svc > ./log/lb_processor_svc.log &
nohup pkill -f lookup_svc > ./log/lookup_svc.log &
nohup pkill -f ss_archive_svc > ./log/ss_archive_svc.log &
nohup pkill -f lookup_svc_retro > ./log/lookup_svc_retro.log &
nohup pkill -f ss_archive_svc_retro > ./log/ss_archive_svc_retro.log &

nohup pkill -f utils_svc > ./log/utils_svc.log &
nohup pkill -f file_svc > ./log/file_svc.log &
nohup pkill -f email_svc > ./log/email_svc.log &
