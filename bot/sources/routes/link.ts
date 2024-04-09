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
  route: "/link",
})
export default class extends Route {
  public async [methods.GET](_request: ApiRequest, response: ApiResponse) {
    const user = await container.client.users.fetch(
      _request.query["id"] as string
    );

    if (isNullish(user)) return;

    await user.send({
      content: "Hello, World!",
    });

    return response.json({
      status: "ok",
    });
  }
}
