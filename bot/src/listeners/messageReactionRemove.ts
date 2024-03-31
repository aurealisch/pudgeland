import type { Action } from "@models/Action";
import { ApplyOptions } from "@sapphire/decorators";
import { Events, Listener } from "@sapphire/framework";
import QuestMessageReactionListener from "@services/QuestMessageReactionListener";

@ApplyOptions<Listener.Options>({
  event: Events.MessageReactionRemove,
})
export default class extends QuestMessageReactionListener {
  public override getAction(): Action {
    return "decrement";
  }
}
