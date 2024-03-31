import type Quest from "@models/Quest";
import { container } from "@sapphire/framework";
import { isNullish } from "@sapphire/utilities";
import { Guild, GuildMember, User } from "discord.js";

export default class QuestManager {
  #quests: Array<Quest>;
  #onQuestComplete: (options: {
    member: GuildMember;
    quest: Quest;
  }) => Promise<void>;

  public constructor(opts: {
    quests: Array<Quest>;
    onQuestComplete: (options: {
      member: GuildMember;
      quest: Quest;
    }) => Promise<void>;
  }) {
    this.#quests = opts.quests;
    this.#onQuestComplete = opts.onQuestComplete;
  }

  public async invoke(opts: { member: GuildMember; guild: Guild }) {
    const db = container.db;
    const member = opts.member;

    const memberId = member.id;
    const user = await db.findUniqueUserOrCreate(memberId);

    this.#quests.forEach(async (quest) => {
      if (member.roles.cache.has(quest.roleId)) return;

      if (user[quest.taskType] < quest.taskRequiredValue) return;

      const role = await opts.guild.roles.cache.get(quest.roleId);

      if (isNullish(role)) return;

      await this.#onQuestComplete({
        quest,
        member,
      });
      await member.roles.add(role);
      await db.increment({
        id: memberId,
        key: "coins",
        value: quest.reward.coins,
      });
    });
  }

  public async invokeReaction(user: User) {
    const guild = container.client.guilds.cache.get(container.guildId);

    if (isNullish(guild)) return;

    const member = guild.members.cache.get(user.id);

    if (isNullish(member)) return;

    this.invoke({
      guild,
      member,
    });
  }
}
