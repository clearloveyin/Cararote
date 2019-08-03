############################################################
# Dockerfile to build iDesign container images

FROM node:lts-alpine as build-stage

WORKDIR /app
#COPY package*.json ./

COPY . .
RUN npm install
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80
#CMD ["nginx", "-g", "daemon off;"]

WORKDIR /usr/share/nginx/html

RUN ls -a ./

CMD sed -i "s|localhost:8080|$SERVER_URL|g" static/config/index.js; cat static/config/index.js; nginx -g "daemon off;"
