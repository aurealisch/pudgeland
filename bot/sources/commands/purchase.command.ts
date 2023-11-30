import { Command } from "../types/command.js";

export let command: Command = {
  name: "покупка",
  description: "Покупка",
  run: (interaction) => {
    interaction.reply({
      content: "покупка",
    });
  },
};
