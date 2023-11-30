import { Command } from "../types/command.js";

export let command: Command = {
  name: "приручение",
  description: "Приручение",
  run: (interaction) => {
    interaction.reply({
      content: "приручение",
    });
  },
};
