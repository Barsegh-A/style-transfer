FROM node:16

WORKDIR /app

COPY package.json ./

RUN npm install

COPY . .

RUN rm -rf build?
RUN npm run build
RUN npm install -g serve

EXPOSE 80

CMD ["serve", "-s", "build", "-l", "80"]
