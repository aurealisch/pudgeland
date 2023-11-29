import { Interaction } from "discord.js";

export function interactionCreate(interaction: Interaction) {
  if (!interaction.isChatInputCommand()) return;

  interaction.client.commands.forEach(async (command) => {
    if (command.name != interaction.commandName) return;

    await command.run(interaction);
  });
}
