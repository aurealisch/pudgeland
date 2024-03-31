import type { Action } from "@models/Action";
import { ApplyOptions } from "@sapphire/decorators";
import { Events, Listener } from "@sapphire/framework";
import QuestMessageListener from "@services/QuestMessageListener";

@ApplyOptions<Listener.Options>({
  event: Events.MessageCreate,
})
export default class extends QuestMessageListener {
  public override getAction(): Action {
    return "increment";
  }
}
