import type { User } from "@prisma/client";
import { ApplyOptions } from "@sapphire/decorators";
import { Events, Listener } from "@sapphire/framework";
import type { Message } from "discord.js";
import QuestListener, { type Execution } from "../services/QuestListener.js";

@ApplyOptions<Listener.Options>({
  event: Events.MessageDelete,
})
export class MessageDeleteListener extends QuestListener {
  override async execute(message: Message): Promise<Execution> {
    const { client, channelId } = message;

    if (
      channelId === client.mediaChannelId ||
      channelId === client.memesChannelId
    ) {
      const attachmentsSize = message.attachments.size;

      if (attachmentsSize === 0) return;

      return {
        action: "decrement",
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
          action: "decrement",
          key: keyword.key,
        };
      }
    }

    return {
      action: "decrement",
      key: "messages",
    };
  }
}
