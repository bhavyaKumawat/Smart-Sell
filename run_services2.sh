#!/bin/bash
run=2

export host_name=""
export port_no=9000
nohup python3 -m ingest > ./log$run/ingest.log &
export host_name=""
export port_no=9001

nohup python3 -m lb_user > ./log$run/lb_user.log &

#lookup
nohup python3 -m lookup > ./log$run/lookup.log &
nohup python3 -m lookup > ./log$run/lookup1.log &

# leaderboard
nohup python3 -m lb_processor > ./log$run/lb_processor.log &
nohup python3 -m lb_processor > ./log$run/lb_processor1.log &

nohup python3 -m archive > ./log$run/archive.log &
export host_name=""
export port_no=9002
nohup python3 -m utils > ./log$run/utils.log &
export host_name=""
export port_no=9003
nohup python3 -m file > ./log$run/file.log &
export host_name=""
export port_no=9004
nohup python3 -m emailss > ./log$run/emailss.log &

nohup python3 -m lookup_retro > ./log$run/lookup_retro.log &

nohup python3 -m archive_retro > ./log$run/archive_retro.log &
