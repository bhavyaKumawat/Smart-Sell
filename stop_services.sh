#!/bin/bash
nohup pkill -f ingest > ./log/ingest.log &
nohup pkill -f lb_user > ./log/lb_user.log &
nohup pkill -f lb_processor > ./log/lb_processor.log &

nohup pkill -f lookup > ./log/lookup.log &
nohup pkill -f lookup > ./log/lookup1.log &

nohup pkill -f archive > ./log/archive.log &
nohup pkill -f lookup_retro > ./log1/lookup_retro.log &
nohup pkill -f archive_retro > ./log1/archive_retro.log &

nohup pkill -f utils > ./log/utils.log &
nohup pkill -f file > ./log/file.log &
nohup pkill -f emailss > ./log/emailss.log &
