FROM node:20 AS build

WORKDIR /app

COPY package*.json ./

RUN npm ci --cache .npm --prefer-offline

COPY . .

RUN npm run build

FROM nginx:1.27

WORKDIR /app

COPY nginx/nginx.conf /etc/nginx/nginx.conf

COPY --from=build /app/dist/olympic-games-starter/browser /app

EXPOSE 80

LABEL description="Conteneur de l'application Angular"