import { Embed, EmbedBuilder } from "discord.js";

export interface Options {
  color: Color;
  title: string;
  description: string;
}

type Color = "profile";

let colors: Record<Color, `#${string}`> = {
  profile: "#24649c",
};

export function createEmbed(options: Options) {
  return new EmbedBuilder()
    .setTitle(options.title)
    .setDescription(options.description)
    .setColor(colors[options.color]);
}
