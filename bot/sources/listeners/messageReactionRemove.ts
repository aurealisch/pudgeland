import type { Action } from "@models/Action";
import QuestMessageReactionListener from "@modules/QuestMessageReactionListener";
import { ApplyOptions } from "@sapphire/decorators";
import { Events, Listener } from "@sapphire/framework";

@ApplyOptions<Listener.Options>({
  event: Events.MessageReactionRemove,
})
export default class extends QuestMessageReactionListener {
  override getAction(): Action {
    return "decrement";
  }
}
