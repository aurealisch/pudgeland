import type { Action } from "@models/Action";
import QuestMessageReactionListener from "@modules/QuestMessageReactionListener";
import { ApplyOptions } from "@sapphire/decorators";
import { Events, Listener } from "@sapphire/framework";

@ApplyOptions<Listener.Options>({
  event: Events.MessageReactionAdd,
})
export default class extends QuestMessageReactionListener {
  override getAction(): Action {
    return "increment";
  }
}
