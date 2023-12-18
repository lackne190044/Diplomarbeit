FROM node:21-alpine3.18

WORKDIR /home/node
RUN npm install axios
RUN npm install -g @vue/cli

COPY . /home/node/vueapp

WORKDIR /home/node/vueapp/app
CMD ["npm", "run", "dev"]
