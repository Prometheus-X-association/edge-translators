ARG NODE_VERSION=23.7.0
ARG ALPINE_VERSION=3.20

FROM node:${NODE_VERSION}-alpine${ALPINE_VERSION} AS runtime_dev

WORKDIR /app

ENV APP_ENV=dev \
    NODE_ENV=development \
    PATH="/app/node_modules/.bin:$PATH"

EXPOSE 8502

COPY --chmod=775 docker/entrypoint.sh /usr/local/bin/docker-entrypoint
ENTRYPOINT ["docker-entrypoint"]

CMD ["yarn", "dev"]

FROM node:${NODE_VERSION}-alpine${ALPINE_VERSION} AS runtime_prod

WORKDIR /app

ENV APP_ENV=dev \
    NODE_ENV=development \
    PATH="/app/node_modules/.bin:$PATH"

COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile --non-interactive --dev

COPY index.html vite.config.ts tsconfig.json tsconfig.app.json tsconfig.node.json ./
COPY public public
COPY src src
EXPOSE 8502

COPY --chmod=775 docker/entrypoint.sh /usr/local/bin/docker-entrypoint
ENTRYPOINT ["docker-entrypoint"]

CMD ["yarn", "dev"]