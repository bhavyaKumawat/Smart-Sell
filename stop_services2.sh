#!/bin/bash
run=2
nohup pkill -f ingest > ./log$run/ingest.log &
nohup pkill -f lb_user > ./log$run/lb_user.log &
nohup pkill -f lb_processor > ./log$run/lb_processor.log &
nohup pkill -f lb_processor > ./log$run/lb_processor1.log &

nohup pkill -f lookup > ./log$run/lookup.log &
nohup pkill -f lookup > ./log$run/lookup1.log &

nohup pkill -f archive > ./log$run/archive.log &
nohup pkill -f lookup_retro > ./log$run/lookup_retro.log &
nohup pkill -f archive_retro > ./log$run/archive_retro.log &

nohup pkill -f utils > ./log$run/utils.log &
nohup pkill -f file > ./log$run/file.log &
nohup pkill -f emailss > ./log$run/emailss.log &
