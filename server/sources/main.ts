import fastify from "fastify";

const server = fastify({
  logger: {
    transport: {
      target: "pino-pretty",
    },
  },
}).get("/", (_, reply) => {
  reply.code(200).send("Hello, World!");
});

const socialNetworks: Array<{
  name: "discord" | "vk" | "tiktok";
  url: string;
}> = [
  { name: "discord", url: "https://discord.gg/cSRCyxdThB" },
  { name: "tiktok", url: "https://vm.tiktok.com/ZTLj926CC" },
  { name: "vk", url: "https://vk.com/pudgeland" },
];

socialNetworks.forEach((socialNetwork) => {
  server.get(`/${socialNetwork.name}`, (_, reply) => {
    reply.redirect(socialNetwork.url);
  });
});

server.listen({
  host: "0.0.0.0",
  port: 10_000,
});
