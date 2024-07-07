# THERE ARE SOME ADDITIONAL ACTIONS YOU NEEED TO DO.
# PLEASE CHECK README, IT IS QUICK

FROM ubuntu:latest

WORKDIR /app

RUN apt update && apt upgrade -y
RUN apt install -y python3.12-venv python3-pip

COPY ./db /app/db/
COPY ./static /app/static
COPY ./templates /app/templates/
COPY account_bp.py app.py funcs.py my_words_bp.py tasks_bp.py /app/

RUN python3.12 -m venv venv
RUN . venv/bin/activate
RUN pip3.12 install --break-system-packages flask flask_login sqlalchemy

EXPOSE 80/tcp
CMD ["python3.12", "app.py"]
