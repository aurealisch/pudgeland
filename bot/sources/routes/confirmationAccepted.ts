import { ApplyOptions } from "@sapphire/decorators";
import { container } from "@sapphire/framework";
import {
  Route,
  methods,
  type ApiRequest,
  type ApiResponse,
} from "@sapphire/plugin-api";
import { isNullish } from "@sapphire/utilities";

@ApplyOptions<Route.Options>({
  route: "/confirmationAccepted",
})
export default class extends Route {
  public async [methods.GET](_request: ApiRequest, response: ApiResponse) {
    const userId = _request.query["userId"] as string;

    const user = await container.client.users.fetch(userId);

    if (isNullish(user)) return;

    await container.db.setMinecraftDisplayName({
      id: userId,
      val: _request.query["minecraftDisplayName"] as string,
    });

    return response.json({
      status: "ok",
    });
  }
}
