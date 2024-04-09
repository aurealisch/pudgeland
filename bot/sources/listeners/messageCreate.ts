import type { Action } from "@models/Action";
import QuestMessageListener from "@modules/QuestMessageListener";
import { ApplyOptions } from "@sapphire/decorators";
import { Events, Listener } from "@sapphire/framework";

@ApplyOptions<Listener.Options>({
  event: Events.MessageCreate,
})
export default class extends QuestMessageListener {
  override getAction(): Action {
    return "increment";
  }
}
