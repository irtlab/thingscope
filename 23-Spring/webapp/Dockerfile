# Dockerfile for nodejs application
FROM node
WORKDIR /webapp_server
COPY package.json .
RUN npm install
COPY . ./
CMD ["npm", "start"]
