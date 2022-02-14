import os

import uvicorn

from lb_user_svc.api import leaderboard

host = os.environ["host_name"]
port = os.environ["lb_user_svc_port_no"]
if __name__ == '__main__':
    uvicorn.run(leaderboard, host=host, port=int(port))
