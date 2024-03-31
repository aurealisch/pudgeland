import quests from "@configurations/quests";
import type Quest from "@models/Quest";
import { PrismaClient } from "@prisma/client";
import { SapphireClient, container } from "@sapphire/framework";
import { isNullish } from "@sapphire/utilities";
import Database from "@services/Database";
import QuestManager from "@services/QuestManager";
import { GatewayIntentBits, GuildMember, Partials } from "discord.js";

export default class extends SapphireClient {
  public constructor() {
    super({
      intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.GuildMessageReactions,
        GatewayIntentBits.MessageContent,
      ],
      partials: [
        Partials.Channel,
        Partials.GuildMember,
        Partials.Message,
        Partials.Reaction,
        Partials.User,
      ],
    });
  }

  public override async login(token?: string | undefined) {
    container.db = new Database(new PrismaClient());

    await container.db.connect();

    container.memesChannelId = "1209222510504050739";
    container.mediaChannelId = "1010818952525529130";
    container.guildId = "1010816890513395803";

    const chatChannelId = "1010817561367171134";

    container.questMng = new QuestManager({
      quests,
      async onQuestComplete(opts: { member: GuildMember; quest: Quest }) {
        const channel = await container.client.channels.fetch(chatChannelId);

        if (isNullish(channel)) return;

        if (!channel.isTextBased()) return;

        await channel.send({
          content: `🎉 <@${opts.member.id}> выполнил задание <@&${opts.quest.roleId}>`,
        });
      },
    });

    return super.login(token);
  }

  public override async destroy() {
    await container.db.disconnect();

    return super.destroy();
  }
}

declare module "@sapphire/pieces" {
  interface Container {
    db: Database;
    questMng: QuestManager;
    mediaChannelId: string;
    memesChannelId: string;
    guildId: string;
  }
}
