import { ChatInputCommandInteraction } from "discord.js";

export type Command = {
  name: string;
  description: string;
  run(interaction: ChatInputCommandInteraction): unknown | Promise<unknown>;
};
