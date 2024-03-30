FROM oven/bun
WORKDIR /usr/src/app
COPY . .
RUN bun install
RUN bun run prisma generate
CMD [ "bun", "run", "start" ]
