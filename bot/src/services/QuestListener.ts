import type { User } from "@prisma/client";
import { Listener } from "@sapphire/framework";
import { isNullish } from "@sapphire/utilities";
import type { Message } from "discord.js";

type Action = "increment" | "decrement";
export type Execution =
  | {
      action: Action;
      key: keyof User;
      value?: number;
    }
  | undefined;

export default class QuestListener extends Listener {
  public async execute(_: Message): Promise<Execution> {
    return;
  }

  public async run(message: Message) {
    const author = message.author;

    if (author.bot) return;

    const execution = await this.execute(message);

    if (isNullish(execution)) return;

    await message.client.questManager.invoke(message);

    await message.client.database[execution.action]({
      id: message.author.id,
      key: execution.key,
      value: execution.value,
    });
  }
}
