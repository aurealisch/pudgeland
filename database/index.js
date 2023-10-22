import "dotenv/config";
import fastify from "fastify";
import { Sequelize, DataTypes } from "sequelize";

const {
  postgresUsername,
  postgresPassword,
  postgresHost,
  postgresPort,

  postgresDatabase,

  headersAuthorization,

  HOST,
  PORT,

  fastifyHost,
  fastifyPort,
} = process.env;

const fastifyInstance = fastify({ logger: true });

const sequelize = new Sequelize({
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

const User = sequelize.define("user", {
  id: { type: DataTypes.STRING, primaryKey: true },

  berry: { type: DataTypes.INTEGER, defaultValue: 0 },
  fox: { type: DataTypes.INTEGER, defaultValue: 1 },

  coin: { type: DataTypes.INTEGER, defaultValue: 0 },

  netheriteScrap: { type: DataTypes.INTEGER, defaultValue: 0 },
  diamond: { type: DataTypes.INTEGER, defaultValue: 0 },
});

fastifyInstance.get("/users/", (fastifyRequest, fastifyReply) => {
  const { id } = fastifyRequest.query;

  User.findOrCreate({ where: { id } }).then(([user]) => {
    return fastifyReply.send({
      berry: user.berry,
      fox: user.fox,

      coin: user.coin,

      netheriteScrap: user.netheriteScrap,
      diamond: user.diamond,
    });
  });
});

fastifyInstance.get(
  "/users/berry/increment/",
  (fastifyRequest, fastifyReply) => {
    const { id, by } = fastifyRequest.query;

    Promise.all([User.increment({ berry: by }, { where: { id } })]);
  }
);
fastifyInstance.get(
  "/users/berry/decrement/",
  (fastifyRequest, fastifyReply) => {
    const { id, by } = fastifyRequest.query;

    Promise.all([User.decrement({ berry: by }, { where: { id } })]);
  }
);

fastifyInstance.get("/users/fox/increment/", (fastifyRequest, fastifyReply) => {
  const { id, by } = fastifyRequest.query;

  Promise.all([User.increment({ fox: by }, { where: { id } })]);
});
fastifyInstance.get("/users/fox/decrement/", (fastifyRequest, fastifyReply) => {
  const { id, by } = fastifyRequest.query;

  Promise.all([User.decrement({ fox: by }, { where: { id } })]);
});

fastifyInstance.get(
  "/users/coin/increment/",
  (fastifyRequest, fastifyReply) => {
    const { id, by } = fastifyRequest.query;

    Promise.all([User.increment({ coin: by }, { where: { id } })]);
  }
);
fastifyInstance.get(
  "/users/coin/decrement/",
  (fastifyRequest, fastifyReply) => {
    const { id, by } = fastifyRequest.query;

    Promise.all([User.decrement({ coin: by }, { where: { id } })]);
  }
);

fastifyInstance.get(
  "/users/diamond/increment/",
  (fastifyRequest, fastifyReply) => {
    const { id, by } = fastifyRequest.query;

    Promise.all([User.increment({ diamond: by }, { where: { id } })]);
  }
);
fastifyInstance.get(
  "/users/diamond/decrement/",
  (fastifyRequest, fastifyReply) => {
    const { id, by } = fastifyRequest.query;

    Promise.all([User.decrement({ diamond: by }, { where: { id } })]);
  }
);

fastifyInstance.get(
  "/users/netheriteScrap/increment/",
  (fastifyRequest, fastifyReply) => {
    const { id, by } = fastifyRequest.query;

    Promise.all([User.increment({ netheriteScrap: by }, { where: { id } })]);
  }
);
fastifyInstance.get(
  "/users/netheriteScrap/decrement/",
  (fastifyRequest, fastifyReply) => {
    const { id, by } = fastifyRequest.query;

    Promise.all([User.decrement({ netheriteScrap: by }, { where: { id } })]);
  }
);

fastifyInstance.get("/leaders/berry/", (fastifyRequest, fastifyReply) => {
  User.findAll({
    limit: 3,
    order: [["berry", "DESC"]],
  }).then((users) => {
    return fastifyReply.send(
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
    limit: 3,
    order: [["fox", "DESC"]],
  }).then((users) => {
    return fastifyReply.send(
      users.map((user) => {
        return {
          id: user.id,
          fox: user.fox,
        };
      })
    );
  });
});

fastifyInstance.get("/leaders/coin/", (fastifyRequest, fastifyReply) => {
  User.findAll({
    limit: 3,
    order: [["coin", "DESC"]],
  }).then((users) => {
    return fastifyReply.send(
      users.map((user) => {
        return {
          id: user.id,
          coin: user.coin,
        };
      })
    );
  });
});

fastifyInstance.get(
  "/leaders/netheriteScrap/",
  (fastifyRequest, fastifyReply) => {
    User.findAll({
      limit: 3,
      order: [["netheriteScrap", "DESC"]],
    }).then((users) => {
      return fastifyReply.send(
        users.map((user) => {
          return {
            id: user.id,
            netheriteScrap: user.netheriteScrap,
          };
        })
      );
    });
  }
);

fastifyInstance.get("/leaders/diamond/", (fastifyRequest, fastifyReply) => {
  User.findAll({
    limit: 3,
    order: [["diamond", "DESC"]],
  }).then((users) => {
    return fastifyReply.send(
      users.map((user) => {
        return {
          id: user.id,
          diamond: user.diamond,
        };
      })
    );
  });
});

fastifyInstance.addHook("onRequest", async (fastifyRequest, fastifyReply) => {
  if (headersAuthorization !== fastifyRequest.headers.authorization) {
    return fastifyReply.code(403).send({ message: 'Forbidden' });
  }
});

fastifyInstance.listen({
  host: HOST || fastifyHost,
  port: PORT || fastifyPort,
});
