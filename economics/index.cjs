require("dotenv").config();

let sequalize = require("sequelize");
let redis = require("redis");

let {
  authorization,
  postgresUsername,
  postgresPassword,
  postgresHost,
  postgresPort,
  postgresDatabase,
  redisUsername,
  redisPassword,
  redisSocketHost,
  redisSocketPort,
  HOST,
  PORT,
  fastifyHost,
  fastifyPort,
} = process.env;

let User = new sequalize.Sequelize({
  dialect: "postgres",

  username: postgresUsername,
  password: postgresPassword,
  host: postgresHost,
  port: postgresPort,
  database: postgresDatabase,

  define: {
    createdAt: false,
    updatedAt: false,
  },
}).define("user", {
  id: { type: sequalize.DataTypes.INTEGER, primaryKey: true },
  berry: sequalize.DataTypes.INTEGER,
  fox: sequalize.DataTypes.INTEGER,
});

let client = redis.createClient({
  username: redisUsername,
  password: redisPassword,
  socket: {
    host: redisSocketHost,
    port: redisSocketPort,
    connectTimeout: 50000,
  },
});

let fastify = require("fastify")({ logger: true });

fastify.get("/users/:id", async (request, reply) => {
  let { id } = request.params;

  let berry = await client.get(`users:${id}:berry`)
  let fox = await client.get(`users:${id}:fox`)

  if (berry != null && fox != null) {
    reply.send({
      berry: Number(berry),
      fox: Number(fox),
    });

    return;
  }

  await User.findOrCreate({
    where: { id },
    defaults: {
      berry: 0,
      fox: 0,
    },
  }).then(async ([user]) => {
    let seconds = 300;

    let berry = user.berry;
    let fox = user.fox;

    await client.setEx(`users:${id}:berry`, seconds, String(berry));
    await client.setEx(`users:${id}:fox`, seconds, String(fox));

    reply.send({
      berry,
      fox,
    });
  });
});

fastify.get("/users/:id/increment/:field/:by", async (request, reply) => {
  let { id, field, by } = request.params;

  User.increment({ field: by }, { where: { id } }).then(([affectedRows]) => {
    affectedRows.forEach(async (affectedRow) => {
      let id = affectedRow.id;

      let seconds = 300;

      // prettier-ignore
      await client.setEx(`users:${id}:berry`, seconds, String(affectedRow.berry));
      await client.setEx(`users:${id}:fox`, seconds, String(affectedRow.fox));
    });
  });
});

fastify.get("/users/:id/decrement/:field/:by", async (request, reply) => {
  let { id, field, by } = request.params;

  User.decrement({ field: by }, { where: { id } }).then(([affectedRows]) => {
    affectedRows.forEach(async (affectedRow) => {
      let id = affectedRow.id;

      let seconds = 300;

      // prettier-ignore
      await client.setEx(`users:${id}:berry`, seconds, String(affectedRow.berry));
      await client.setEx(`users:${id}:fox`, seconds, String(affectedRow.fox));
    });
  });
});

fastify.get("/leaders/:field", (request, reply) => {
  let { field } = request.params;

  User.findAll({
    limit: 6,
    order: [[field, "DESC"]],
  }).then((users) => {
    users.map((user) => {
      return {
        berry: user.berry,
        fox: user.fox,
      };
    });

    reply.send(users);
  });
});

fastify.addHook("onRequest", async (request, reply) => {
  if (authorization !== request.headers.authorization) {
    reply.code(403).send();
  }
});

fastify.addHook("onReady", async () => {
  await client.connect();
});
fastify.addHook("onClose", async () => {
  await client.disconnect();
});

fastify.listen({
  host: HOST || fastifyHost,
  port: PORT || fastifyPort,
});
