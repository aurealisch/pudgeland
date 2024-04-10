import { ApplyOptions } from "@sapphire/decorators";
import {
    InteractionHandler,
    InteractionHandlerTypes,
} from "@sapphire/framework";
import type { ButtonInteraction } from "discord.js";
import { Code } from "../enums";

@ApplyOptions<InteractionHandler.Options>({
  interactionHandlerType: InteractionHandlerTypes.Button,
})
export default class extends InteractionHandler {
  override parse(buttonInteraction: ButtonInteraction) {
    if (buttonInteraction.customId !== "confirmation-rejected") {
      return this.none();
    }

    return this.some();
  }

  async run(buttonInteraction: ButtonInteraction) {
    this.container.webSocket.send(
      JSON.stringify({
        code: Code.ConfirmationRejected,
        data: {
          userId: buttonInteraction.user.id,
        },
      })
    );

    await buttonInteraction.reply({
      content: "Отказано",
      ephemeral: true,
    });
  }
}
