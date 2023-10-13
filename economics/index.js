require("dotenv").config();

let sequalize = require("sequelize");

let {
  _USERNAME,
  _PASSWORD,
  _HOST,
  _PORT,
  _DATABASE,
} = process.env;

let uri =
  `postgresql://${_USERNAME}:${_PASSWORD}@${_HOST}:${_PORT}/${_DATABASE}`;

let User = new sequalize.Sequelize(uri).define("user", {
  id: { type: sequalize.DataTypes.INTEGER, primaryKey: true },
  berry: { type: sequalize.DataTypes.INTEGER },
  fox: { type: sequalize.DataTypes.INTEGER },
}, {
  createdAt: false,
  updatedAt: false,
})

let fastify = require("fastify")({ logger: true });

fastify.get("/users/:id", function handler(request, reply) {
  let { id } = request.params;

  User.findOrCreate({
    where: { id },
    defaults: {
      berry: 0,
      fox: 0,
    },
  }).then(([user]) => {
    reply.send({
      berry: user.berry,
      fox: user.fox,
    });
  });
});

fastify.get("/users/:id/increment/:field/:by", async function handler(request, reply) {
  let { id, field, by } = request.params;

  switch (field) {
    case "berry": await User.increment({ berry: by }, { where: { id } });
    case "fox": await User.increment({ fox: by }, { where: { id } });
  }
})

fastify.get("/users/:id/decrement/:field/:by", async function handler(request, reply) {
  let { id, field, by } = request.params;

  switch (field) {
    case "berry": await User.decrement({ berry: by }, { where: { id } });
    case "fox": await User.decrement({ fox: by }, { where: { id } });
  }
})

fastify.get("/leaders/:field", function handler(request, reply) {
  let { field } = request.params;

  User.findAll({
    limit: 6,
    order: [[field, "DESC"]]
  }).then((users) => {
    users.map(function callback(user) {
      return {
        berry: user.berry,
        fox: user.fox,
      };
    });

    reply.send(users);
  });
});

fastify.listen({ port: 3000 });
