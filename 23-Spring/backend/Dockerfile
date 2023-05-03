FROM node
WORKDIR /webapp_server
COPY package.json .
RUN npm install
COPY . .
ADD https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem .
CMD ["npm", "run", "api_dev"]