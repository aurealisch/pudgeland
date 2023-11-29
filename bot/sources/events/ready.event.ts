import { PrismaClient } from "@prisma/client";
import { Client, Routes, SlashCommandBuilder } from "discord.js";
import { guildMemberAdd } from "./guildMemberAdd.event.js";
import { guildMemberRemove } from "./guildMemberRemove.event.js";
import { interactionCreate } from "./interactionCreate.event.js";
import { Database } from "../modules/database.js";

export function ready(client: Client) {
  client.commands = [];
  Promise.all([
    import("../commands/collecting.command.js"),
    import("../commands/domestication.command.js"),
    import("../commands/leaders.command.js"),
    import("../commands/profile.command.js"),
    import("../commands/purchase.command.js"),
    import("../commands/sale.command.js"),
  ]).then((commands) => {
    commands.forEach(({ command }) => {
      client.commands.push(command);
    });
  });

  let { applicationId, guildId } = client;

  let body = client.commands.map((command) => {
    return new SlashCommandBuilder()
      .setName(command.name)
      .setDescription(command.description)
      .toJSON();
  });

  client.rest.put(Routes.applicationGuildCommands(applicationId, guildId), {
    body: body,
  });

  let prismaClient = new PrismaClient();

  prismaClient.$connect().then(() => {
    client.database = new Database(prismaClient);
  });

  client.on("debug", client.logger.debug);
  client.on("warn", client.logger.warn);
  client.on("error", client.logger.error);

  client.on("guildMemberAdd", guildMemberAdd);
  client.on("guildMemberRemove", guildMemberRemove);
  client.on("interactionCreate", interactionCreate);
}
