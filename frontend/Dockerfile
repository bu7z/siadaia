# Build-Stage
FROM node:18 as builder

WORKDIR /app

# Nur relevante Dateien kopieren – nicht node_modules oder Build-Output
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Production-Stage
FROM nginx:alpine

RUN rm -f /etc/nginx/conf.d/*
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
