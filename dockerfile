FROM python:3
ENV PYTOHNDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y python3-pip && apt-get install -y gunicorn && apt-get clean
RUN apt-get install python3-mysqldb && apt-get install -y pkg-config && apt-get install curl && apt-get install unzip && apt-get install tar
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && ./aws/install
#RUN apt-get install awscli
COPY $PWD/requirments.txt /rockets/requirments.txt
COPY $PWD/rockets/ ./rockets/

# for ARM systems, set ARCH to: `arm64`, `armv6` or `armv7`
RUN ARCH=amd64
RUN PLATFORM=$(uname -s)_$ARCH
RUN curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
RUN mv /tmp/eksctl /usr/local/bin

WORKDIR /rockets
RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install -r requirments.txt
#CMD ["/bin/tail","-f","/dev/null"]
CMD [ "gunicorn","--bind","0:2340", "rockets.wsgi:application" ]



