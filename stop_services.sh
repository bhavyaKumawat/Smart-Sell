#!/bin/bash
nohup pkill -f ss_ingest > ./log/ss_ingest.log &
nohup pkill -f lb_user_svc > ./log/lb_user_svc.log &
nohup pkill -f lb_processor_svc > ./log/lb_processor_svc.log &
nohup pkill -f lookup_svc > ./log/lookup_svc.log &
nohup pkill -f ss_archive_svc > ./log/ss_archive_svc.log &
