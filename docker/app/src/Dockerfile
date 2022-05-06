FROM @dockerRegistry/@ImageBaseAppPython39 as build-venv
USER root
COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check --no-cache-dir -r /requirements.txt

FROM debian:11-slim as odbc-driver
COPY files/prepare_libs.sh /
RUN apt-get update \
    && apt-get install -y curl gnupg libodbc1 \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && /bin/bash /prepare_libs.sh /libs

# Copy the virtualenv into a distroless image
FROM gcr.io/distroless/python3-debian11

WORKDIR /app
COPY --from=build-venv /venv /venv
COPY --from=odbc-driver /opt/microsoft /opt/microsoft
COPY --from=odbc-driver /libs/* /usr/lib/x86_64-linux-gnu/
COPY --from=odbc-driver /lib/x86_64-linux-gnu/libgpg-error.so* /lib/x86_64-linux-gnu/
COPY --from=odbc-driver /etc/odbc* /etc/

COPY . .
