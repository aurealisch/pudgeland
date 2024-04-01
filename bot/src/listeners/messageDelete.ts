import type { Action } from "@models/Action";
import { ApplyOptions } from "@sapphire/decorators";
import { Events, Listener } from "@sapphire/framework";
import QuestMessageListener from "@svcs/QuestMessageListener";

@ApplyOptions<Listener.Options>({
  event: Events.MessageDelete,
})
export default class extends QuestMessageListener {
  public override getAction(): Action {
    return "decrement";
  }
}
