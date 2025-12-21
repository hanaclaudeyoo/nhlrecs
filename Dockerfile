# FROM python:3.12.4-alpine3.20
FROM python:3.11.5-alpine3.18

# Install build dependencies for matplotlib and other packages
RUN apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    linux-headers \
    freetype-dev \
    libpng-dev \
    openblas-dev \
    lapack-dev \
    gfortran

# permissions and nonroot user for tightened security
RUN adduser -D nonroot
RUN mkdir /home/app/ && chown -R nonroot:nonroot /home/app
WORKDIR /home/app
USER nonroot

# copy all the files to the container
COPY --chown=nonroot:nonroot . .

# venv
ENV VIRTUAL_ENV=/home/app/venv

# python setup
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

EXPOSE 7860
CMD ["python", "-m", "ui.app"]
# CMD ["python", "gradio_demo.py"]
# CMD ["gradio", "gradio_demo.py"]