import { ActionRowBuilder, ButtonBuilder, ButtonStyle } from "discord.js";

export default function (
  buttons: Array<{
    customId: string;
    emoji: string;
    label: string;
  }>
) {
  return [
    new ActionRowBuilder<ButtonBuilder>().addComponents(
      buttons.map((button) => {
        return new ButtonBuilder()
          .setCustomId(button.customId)
          .setEmoji(button.emoji)
          .setLabel(button.label)
          .setStyle(ButtonStyle.Secondary);
      })
    ),
  ];
}
