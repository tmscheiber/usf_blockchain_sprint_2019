FROM alpine:3.9.2

# update
RUN apk add --update python3 py3-pip
RUN apk add --update gcc

# Install dependencies
# Install app dependencies
RUN pip3 install --upgrade pip

# enabling build of pycrypto or pycryptodome support
#     https://github.com/pyca/cryptography/issues/4264
COPY ./build-cryptography.sh .
RUN apk -U add build-base linux-headers libffi-dev mariadb-dev \
    gettext curl gcc musl-dev python3-dev libressl-dev perl
RUN pip install virtualenv
RUN ./build-cryptography.sh
RUN pip install --no-index --find-links=./ cryptography

# ensure required python modules are installed
COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r /usr/src/app/requirements.txt

# copy in blockchain app
COPY ./medical_record_chain_client.py /usr/src/app/
COPY ./templates /usr/src/app/templates
COPY ./static /usr/src/app/static

WORKDIR /usr/src/app
EXPOSE 8080
CMD ["python3", "./medical_record_chain_client.py", "-p 8080"]