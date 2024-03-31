import { ApplyOptions } from "@sapphire/decorators";
import {
    Route,
    methods,
    type ApiRequest,
    type ApiResponse,
} from "@sapphire/plugin-api";

@ApplyOptions<Route.Options>({
  route: "/",
})
export default class extends Route {
  public [methods.GET](_request: ApiRequest, response: ApiResponse) {
    response.json({ message: "Hello, World!" });
  }
}
