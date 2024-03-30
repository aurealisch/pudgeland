import { ApplyOptions } from "@sapphire/decorators";
import { Events, Listener } from "@sapphire/framework";
import type { Message } from "discord.js";
import QuestListener, { type Execution } from "../services/QuestListener.js";

@ApplyOptions<Listener.Options>({
  event: Events.MessageReactionRemove,
})
export class MessageReactionRemoveListener extends QuestListener {
  override async execute(_: Message): Promise<Execution> {
    return {
      action: "decrement",
      key: "messageReactions",
    };
  }
}
