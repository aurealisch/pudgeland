import { ApplyOptions } from "@sapphire/decorators";
import { Command, container } from "@sapphire/framework";
import CreateEmbed from "@utilities/CreateEmbed";
import { dedent } from "dedented";

@ApplyOptions<Command.Options>({
  name: "профиль",
})
export default class extends Command {
  public override async chatInputRun(
    interaction: Command.ChatInputCommandInteraction
  ) {
    const user = await container.db.findUniqueUserOrCreate(interaction.user.id);

    await interaction.reply({
      embeds: [
        CreateEmbed({
          description: dedent`
            :coin: Монеты: **\`${user.coins}\`**
            \`\`\`
            "1.1": ${user.firstRule}
            "гг сервер умер": ${user.ggServerDied}
            "когда сервер": ${user.whenServer}
            Медиа или мемов: ${user.mediaOrMemes}
            Сообщений: ${user.messages}
            Реакций: ${user.messageReactions}
            \`\`\`
          `,
          title: "Профиль",
        }),
      ],
    });
  }
}
