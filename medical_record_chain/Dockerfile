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
RUN ls /usr/src/app
RUN pip3 install --no-cache-dir -r /usr/src/app/requirements.txt

# copy in blockchain app
COPY blockchain/medical_record_chain.py /usr/src/app/
COPY blockchain/templates /usr/src/app/templates
COPY blockchain/static /usr/src/app/static
RUN ls /usr/src/app

EXPOSE 5000
CMD ["python3", "./medical_record_chain.py", "-p 5000"]