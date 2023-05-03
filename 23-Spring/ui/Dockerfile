FROM node
WORKDIR /webapp
COPY package.json .
RUN npm install
COPY . ./
CMD ["npm", "start"]