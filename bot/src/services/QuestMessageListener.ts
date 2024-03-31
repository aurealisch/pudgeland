import type { Action } from "@models/Action";
import type { User } from "@prisma/client";
import { Listener, container } from "@sapphire/framework";
import { isNullish } from "@sapphire/utilities";
import type { Message } from "discord.js";

export default class extends Listener {
  public getAction(): Action | undefined {
    return;
  }

  async execute(message: Message): Promise<
    | {
        key: keyof User;
        value?: number;
      }
    | undefined
  > {
    const channelId = message.channelId;

    if (
      channelId === container.mediaChannelId ||
      channelId === container.memesChannelId
    ) {
      const attachmentsSize = message.attachments.size;

      if (attachmentsSize === 0) return;

      return {
        key: "mediaOrMemes",
        value: attachmentsSize,
      };
    }

    const content = message.content.toLowerCase();

    const keywords: Array<{
      include: string;
      key: keyof User;
    }> = [
      { include: "гг сервер умер", key: "ggServerDied" },
      { include: "когда сервер", key: "whenServer" },
      { include: "1.1", key: "firstRule" },
    ];

    for (const keyword of keywords) {
      if (content.includes(keyword.include)) {
        return {
          key: keyword.key,
        };
      }
    }

    return {
      key: "messages",
    };
  }

  public async run(message: Message) {
    const action = this.getAction();

    if (isNullish(action)) return;

    const { author, member, guild } = message;

    if (author.bot) return;

    const execution = await this.execute(message);

    if (isNullish(execution)) return;

    if (isNullish(member)) return;
    if (isNullish(guild)) return;

    await container.questMng.invoke({
      member,
      guild,
    });

    await container.db[action]({
      id: message.author.id,
      key: execution.key,
      value: execution.value,
    });
  }
}
