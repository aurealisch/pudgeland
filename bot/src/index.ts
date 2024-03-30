import { SapphireClient } from "@sapphire/framework";
import fastify from "fastify";

new SapphireClient({
  regexPrefix: /пенис\s/,
  disableMentionPrefix: true,
  intents: ["Guilds", "GuildMessages", "MessageContent"],
  loadMessageCommandListeners: true,
}).login(process.env.TOKEN);

fastify({
  logger: {
    transport: {
      target: "pino-pretty",
    },
  },
})
  .get("/", (_, reply) => {
    reply.code(200).send("Hello, World!");
  })
  .listen({
    host: "0.0.0.0",
    port: 10_000,
  });
