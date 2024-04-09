import type { Action } from "@models/Action";
import { Listener, container } from "@sapphire/framework";
import { isNullish } from "@sapphire/utilities";
import type { MessageReaction, User } from "discord.js";

export default class QuestMessageReactionListener extends Listener {
  getAction(): Action | undefined {
    return;
  }

  async run(reaction: MessageReaction, user: User) {
    const action = this.getAction();

    if (isNullish(action)) return;

    if (user.bot) return;

    await container.db[action]({
      id: user.id,
      key: "messageReactions",
    });

    await container.questMng.invokeReaction(user);
  }
}
