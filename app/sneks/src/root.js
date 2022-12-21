import * as React from "react";

import { Amplify } from "aws-amplify";
import { Authenticator } from "@aws-amplify/ui-react";

import App from "./App";

import { config } from "./aws-config";

Amplify.configure(config);

export default function Root() {
  return (
    <React.StrictMode>
      <Authenticator.Provider>
        <App />
      </Authenticator.Provider>
    </React.StrictMode>
  );
}
