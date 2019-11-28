FROM nodered/node-red:latest-minimal
WORKDIR /data

COPY package.json .
RUN yarn install

COPY settings.js .
COPY subflow.json /data/flows.json

WORKDIR /usr/src/node-red
VOLUME /data

