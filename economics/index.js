import "dotenv/config";
import fastify from "fastify";
import { Sequelize, DataTypes } from "sequelize";
import { createClient } from "redis";

const {
  postgresUsername,
  postgresPassword,
  postgresHost,
  postgresPort,

  postgresDatabase,

  redisUsername,
  redisPassword,
  redisSocketHost,
  redisSocketPort,

  headersAuthorization,

  HOST,
  PORT,

  fastifyHost,
  fastifyPort,
} = process.env;

const fastifyInstance = fastify({ logger: true });

const sequalize = new Sequelize({
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
});

const User = sequalize.define("user", {
  id: { type: DataTypes.INTEGER, primaryKey: true },
  berry: { type: DataTypes.INTEGER },
  fox: { type: DataTypes.INTEGER },
});

const client = createClient({
  username: redisUsername,
  password: redisPassword,
  socket: {
    host: redisSocketHost,
    port: redisSocketPort,

    connectTimeout: 50_000,
  },
});

const exSeconds = 300;

fastifyInstance.get("/users/", async (fastifyRequest, fastifyReply) => {
  const { id } = fastifyRequest.query;

  const berry = await client.get(`users:${id}:berry`);
  const fox = await client.get(`users:${id}:fox`);

  if ((berry !== null, fox !== null)) {
    fastifyReply.send({
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
    const berry = user.berry;
    const fox = user.fox;

    await client.setEx(`users:${id}:berry`, exSeconds, String(berry));
    await client.setEx(`users:${id}:fox`, exSeconds, String(fox));

    fastifyReply.send({
      berry,
      fox,
    });
  });
});

fastifyInstance.get(
  "/users/berry/increment/",
  async (fastifyRequest, fastifyReply) => {
    const { id, by } = fastifyRequest.query;

    await User.increment({ berry: by }, { where: { id } }).then(
      ([[affectedRows], affectedCount]) => {
        affectedRows.forEach((affectedRow) => {
          const id = affectedRow.id;

          Promise.all([
            // prettier-ignore
            client.setEx(`users:${id}:berry`, exSeconds, String(affectedRow.berry)),
            client.setEx(`users:${id}:fox`, exSeconds, String(affectedRow.fox)),
          ]);
        });
      }
    );
  }
);
fastifyInstance.get(
  "/users/berry/decrement/",
  async (fastifyRequest, fastifyReply) => {
    const { id, by } = fastifyRequest.query;

    await User.decrement({ berry: by }, { where: { id } }).then(
      ([[affectedRows], affectedCount]) => {
        affectedRows.forEach((affectedRow) => {
          const id = affectedRow.id;

          Promise.all([
            // prettier-ignore
            client.setEx(`users:${id}:berry`, exSeconds, String(affectedRow.berry)),
            client.setEx(`users:${id}:fox`, exSeconds, String(affectedRow.fox)),
          ]);
        });
      }
    );
  }
);

fastifyInstance.get(
  "/users/fox/increment/",
  async (fastifyRequest, fastifyReply) => {
    const { id, by } = fastifyRequest.query;

    await User.increment({ fox: by }, { where: { id } }).then(
      ([[affectedRows], affectedCount]) => {
        affectedRows.forEach((affectedRow) => {
          const id = affectedRow.id;

          Promise.all([
            // prettier-ignore
            client.setEx(`users:${id}:berry`, exSeconds, String(affectedRow.berry)),
            client.setEx(`users:${id}:fox`, exSeconds, String(affectedRow.fox)),
          ]);
        });
      }
    );
  }
);
fastifyInstance.get(
  "/users/fox/decrement/",
  async (fastifyRequest, fastifyReply) => {
    const { id, by } = fastifyRequest.query;

    await User.decrement({ fox: by }, { where: { id } }).then(
      ([[affectedRows], affectedCount]) => {
        affectedRows.forEach((affectedRow) => {
          const id = affectedRow.id;

          Promise.all([
            // prettier-ignore
            client.setEx(`users:${id}:berry`, exSeconds, String(affectedRow.berry)),
            client.setEx(`users:${id}:fox`, exSeconds, String(affectedRow.fox)),
          ]);
        });
      }
    );
  }
);

fastifyInstance.get("/leaders/berry/", (fastifyRequest, fastifyReply) => {
  User.findAll({
    limit: 6,
    order: [["berry", "DESC"]],
  }).then((users) => {
    fastifyReply.send(
      users.map((user) => {
        return {
          id: user.id,
          berry: user.berry,
        };
      })
    );
  });
});

fastifyInstance.get("/leaders/fox/", (fastifyRequest, fastifyReply) => {
  User.findAll({
    limit: 6,
    order: [["fox", "DESC"]],
  }).then((users) => {
    fastifyReply.send(
      users.map((user) => {
        return {
          id: user.id,
          fox: user.fox,
        };
      })
    );
  });
});

fastifyInstance.addHook("onRequest", async (fastifyRequest, fastifyReply) => {
  if (headersAuthorization !== fastifyRequest.headers.authorization) {
    fastifyReply.code(403).send();
  }
});

fastifyInstance.addHook("onReady", (done) => client.connect().then(done()));
fastifyInstance.addHook("onClose", (done) => client.disconnect().then(done()));

fastifyInstance.listen({
  host: HOST || fastifyHost,
  port: PORT || fastifyPort,
});
