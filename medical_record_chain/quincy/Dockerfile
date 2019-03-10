FROM alpine:3.9.2

# update
RUN apk add --update python3 py3-pip
RUN apk add --update gcc

# Install dependencies
# Install app dependencies
RUN pip3 install --upgrade pip

# ensure required python modules are installed
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r ./requirements.txt

# copy in blockchain app
COPY ./quincy.py ./

EXPOSE 8000
CMD ["python3", "./quincy.py", "-p 8000"]