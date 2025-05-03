FROM node:20.19.0
LABEL authors="mbchl"

WORKDIR /frontend

COPY . .

RUN npm install

EXPOSE 5174

CMD ["npm", "run", "dev"]