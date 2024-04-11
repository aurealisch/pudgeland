import { ApplyOptions } from "@sapphire/decorators";
import { container } from "@sapphire/framework";
import {
  Route,
  methods,
  type ApiRequest,
  type ApiResponse,
} from "@sapphire/plugin-api";
import { isNullish } from "@sapphire/utilities";
import ComposeButtons from "@utilities/ComposeButtons";

@ApplyOptions<Route.Options>({
  route: "/sendConfirmation",
})
export default class extends Route {
  public async [methods.GET](_request: ApiRequest, response: ApiResponse) {
    const user = await container.client.users.fetch(
      _request.query["userId"] as string
    );

    if (isNullish(user)) return;

    await user.send({
      content: "Hello, World!",
      components: ComposeButtons([
        { customId: "confirmation-accepted", emoji: "✅", label: "Принять" },
        { customId: "confirmation-canceled", emoji: "❌", label: "Отменить" },
      ]),
    });

    return response.json({
      status: "ok",
    });
  }
}
