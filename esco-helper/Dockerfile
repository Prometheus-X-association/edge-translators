ARG NODE_VERSION=23.7.0
ARG ALPINE_VERSION=3.20

FROM node:${NODE_VERSION}-alpine${ALPINE_VERSION}

RUN apk add --no-cache bash curl

# USER node

WORKDIR /usr/src/app

COPY --chown=node:node package*.json ./
RUN npm ci --omit=dev && npm cache clean --force

COPY --chown=node:node constants/ ./constants
COPY --chown=node:node controllers/ ./controllers
COPY --chown=node:node lib/ ./lib
COPY --chown=node:node routes/ ./routes
COPY --chown=node:node utils/ ./utils
COPY --chown=node:node index.js .

EXPOSE 8080

HEALTHCHECK --start-period=60s CMD curl -f http://esco-helper:8080/api/v1/swagger || exit 1

ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["node", "index.js"]