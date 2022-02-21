FROM python:3.9

WORKDIR /enidsieveapp

# according to the Docker offical docs, we should copy the requirements.txt file
# which will not change as frequently as other files in the working directory,
# and we will be able to make use of the docker's layer cache which will lead to
# faster image bulding.
# PS: every line (intermediate container) afte line 14 (COPY ./service /enidsieveapp/service) will
# not make use of the docker layer cache, if there was any changes to the working dir.
COPY ./requirements.txt /enidsieveapp/requirements.txt

RUN pip install -r /enidsieveapp/requirements.txt

COPY ./service /enidsieveapp/service

CMD ["uvicorn", "service.main:app", "--host", "0.0.0.0", "--port", "80"]