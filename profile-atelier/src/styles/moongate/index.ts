import { StyleModule } from "../../types";
import { getAuthenticStyleById } from "../authenticTemplates";

export const moongateStyle: StyleModule = getAuthenticStyleById("moongate")!;
export default moongateStyle;
