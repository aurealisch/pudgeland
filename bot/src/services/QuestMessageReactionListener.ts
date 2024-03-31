import type { Action } from "@models/Action";
import { Listener, container } from "@sapphire/framework";
import { isNullish } from "@sapphire/utilities";
import type { MessageReaction, User } from "discord.js";

export default class QuestMessageReactionListener extends Listener {
  public getAction(): Action | undefined {
    return;
  }

  public async run(reaction: MessageReaction, user: User) {
    const action = this.getAction();

    if (isNullish(action)) return;

    if (user.bot) return;

    await container.questMng.invokeReaction(user);

    await container.db[action]({
      id: user.id,
      key: "messageReactions",
    });
  }
}
