import { isNullish } from "@sapphire/utilities";
import { Message } from "discord.js";
import type Quest from "../models/Quest.js";

export default class QuestManager {
  constructor(
    private options: {
      quests: Array<Quest>;
      onInvoke: (options: { message: Message; quest: Quest }) => Promise<any>;
    }
  ) {}

  async invoke(message: Message) {
    const {
      member,
      guild,
      client: { database },
    } = message;

    if (isNullish(member)) return;
    if (isNullish(guild)) return;

    const authorId = message.author.id;
    const user = await database.findUniqueUserOrCreate(authorId);

    this.options.quests.forEach(async (quest) => {
      if (member.roles.cache.has(quest.roleId)) return;

      if (user[quest.taskType] >= quest.taskRequiredValue) {
        const role = await guild.roles.cache.get(quest.roleId);

        if (isNullish(role)) return;

        await this.options.onInvoke({
          message,
          quest,
        });
        await member.roles.add(role);
        await database.increment({
          id: authorId,
          key: "coins",
          value: quest.reward.coins,
        });
      }
    });
  }
}
