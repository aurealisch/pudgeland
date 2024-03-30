import { ApplyOptions } from "@sapphire/decorators";
import { Command } from "@sapphire/framework";
import { Message } from "discord.js";

@ApplyOptions<Command.Options>({
  name: "профиль",
})
export class ProgressCommand extends Command {
  public override async messageRun(message: Message) {
    const user = await message.client.database.findUniqueUserOrCreate(
      message.author.id
    );

    await message.reply({
      content: `
      :coin: Монеты: ${user.coins}
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
