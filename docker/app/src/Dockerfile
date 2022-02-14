FROM @dockerRegistry/@ImageBaseAppPython39 as build-venv
USER root
COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check --no-cache-dir -r /requirements.txt

# Copy the virtualenv into a distroless image
FROM gcr.io/distroless/python3-debian11
WORKDIR /app
COPY --from=build-venv /venv /venv
COPY . .