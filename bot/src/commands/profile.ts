import { ApplyOptions } from "@sapphire/decorators";
import { Command } from "@sapphire/framework";
import { dedent } from "dedented";

@ApplyOptions<Command.Options>({
  name: "профиль",
})
export class ProfileCommand extends Command {
  public override async chatInputRun(
    interaction: Command.ChatInputCommandInteraction
  ) {
    const user = await interaction.client.database.findUniqueUserOrCreate(
      interaction.user.id
    );

    await interaction.reply({
      content: dedent`
        :coin: Монеты: **\`${user.coins}\`**
        \`\`\`
        "1.1": ${user.firstRule}
        "гг сервер умер": ${user.ggServerDied}
        "когда сервер": ${user.whenServer}
        Медиа или мемов: ${user.mediaOrMemes}
        Сообщений: ${user.messages}
        Реакций на сообщения: ${user.messageReactions}
        \`\`\`
      `,
    });
  }
}
