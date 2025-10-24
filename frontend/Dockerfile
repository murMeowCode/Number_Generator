FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm i
RUN npm install aos

COPY . .

RUN npm run build

FROM nginx:alpine

COPY --from=0 /app/dist /usr/share/nginx/html

RUN mkdir -p /var/cache/nginx

COPY nginx.conf /etc/nginx/nginx.conf

COPY ssl/ /etc/nginx/ssl/

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
