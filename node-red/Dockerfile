FROM nodered/node-red:latest-minimal
WORKDIR /data

COPY package.json .

RUN yarn install

COPY settings.js /data
COPY subflow_notify_telegram.json /data

WORKDIR /usr/src/node-red
VOLUME /data

