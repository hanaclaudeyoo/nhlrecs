FROM python:3.12.4-alpine3.20

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

# upgrade pip
RUN pip install --upgrade pip
# install
RUN pip install --upgrade pandas==2.2.2
RUN pip install --upgrade gradio==4.42.0

EXPOSE 7860
CMD ["python", "gradio_demo.py"]
# CMD ["gradio", "gradio_demo.py"]