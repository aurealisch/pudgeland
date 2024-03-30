import { PrismaClient } from "@prisma/client";
import { ApplyOptions } from "@sapphire/decorators";
import { Events, Listener } from "@sapphire/framework";
import type { Client, Message } from "discord.js";
import quests from "../configurations/quests.js";
import type Quest from "../models/Quest.js";
import Database from "../services/Database.js";
import QuestManager from "../services/QuestManager.js";

@ApplyOptions<Listener.Options>({
  event: Events.ClientReady,
})
export class ClientReadyListener extends Listener {
  public async run(client: Client) {
    client.database = new Database(new PrismaClient());

    await client.database.connect();

    client.memesChannelId = "1209222510504050739";
    client.mediaChannelId = "1010818952525529130";

    const informationChannelId = "1010839170417172520";

    client.questManager = new QuestManager({
      quests,

      async onInvoke(options: { message: Message; quest: Quest }) {
        await options.message.reply({
          content: `🎉 Ты выполнил задание <@&${options.quest.roleId}> Подробнее: <#${informationChannelId}>`,
        });
      },
    });
  }
}
