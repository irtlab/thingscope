# Dockerfile for nodejs application
FROM node
WORKDIR /webapp_client
COPY package.json .
RUN npm install
COPY . ./
CMD ["npm", "start"]
