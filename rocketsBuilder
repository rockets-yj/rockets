FROM python:3
ENV PYTOHNDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y python3-pip && apt-get install -y gunicorn && apt-get clean
RUN apt-get install python3-mysqldb && apt-get install -y pkg-config
#RUN apt-get install awscli
COPY $PWD/requirments.txt /rockets/requirments.txt
COPY $PWD/rockets/ ./rockets/
WORKDIR /rockets
RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install -r requirments.txt
#CMD ["/bin/tail","-f","/dev/null"]
CMD [ "gunicorn","--bind","0:2340", "rockets.wsgi:application" ]



