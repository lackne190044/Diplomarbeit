# FROM node:21-alpine3.18

# WORKDIR /home/node
# RUN npm install axios
# RUN npm install -g @vue/cli

# # Install vite
# RUN npm install -g create-vite
# RUN create-vite vueapp

# COPY . /home/node/vueapp

# WORKDIR /home/node/vueapp/app
# CMD ["npm", "run", "dev"]
FROM node:21-alpine3.18

WORKDIR /home/node

RUN npm install -g @vue/cli

# Copy the entire Vue.js app into the container
COPY . /home/node/vueapp

WORKDIR /home/node/vueapp

# Install dependencies
RUN npm install

CMD ["npm", "run", "dev"]
