FROM nodered/node-red:latest-minimal
WORKDIR /data

COPY package.json .
COPY settings.js .
COPY subflow_notify_telegram.json .
RUN yarn install

WORKDIR /usr/src/node-red
VOLUME /data

