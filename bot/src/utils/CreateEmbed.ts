import { EmbedBuilder } from "discord.js";

type Color = "default";

const colors: Record<Color, `#${string}`> = {
  default: "#b34646",
};

export default function (opts: {
  description: string;
  title: string;
  color?: Color;
}) {
  return new EmbedBuilder()
    .setColor(colors[opts.color || "default"])
    .setDescription(opts.description)
    .setTitle(opts.title);
}
