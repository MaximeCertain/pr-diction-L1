FROM node:14-alpine

WORKDIR /usr/src/app

COPY package*.json /usr/src/app/

RUN npm install

COPY . /usr/src/app

RUN npm run-script build
EXPOSE  9002

CMD [ "npm", "start" ]