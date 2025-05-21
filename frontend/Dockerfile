# Build-Stage
FROM node:18 as builder

WORKDIR /app
COPY . .

RUN npm install
RUN npm run build

# Production-Stage
FROM nginx:alpine

# Eigene NGINX-Konfiguration
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# HTML-Inhalte
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]