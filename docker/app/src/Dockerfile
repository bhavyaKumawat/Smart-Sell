FROM @dockerRegistry/@ImageBaseAppPython39 as build-venv
USER root
COPY requirements.txt /requirements.txt
#### pyodbc setup
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list

sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
# optional: for bcp and sqlcmd
sudo ACCEPT_EULA=Y apt-get install -y mssql-tools18
echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
source ~/.bashrc
#### end of pyodbc
RUN /venv/bin/pip install --disable-pip-version-check --no-cache-dir -r /requirements.txt

# Copy the virtualenv into a distroless image
FROM gcr.io/distroless/python3-debian11
WORKDIR /app
COPY --from=build-venv /venv /venv
COPY . .