import * as React from "react";

import { Amplify } from "aws-amplify";
import { Authenticator } from "@aws-amplify/ui-react";

import "@cloudscape-design/global-styles/index.css";
import "@aws-amplify/ui-react/styles.css";

import App from "../App";

Amplify.configure({
  Auth: {
    region: "us-east-1",
    userPoolId: "us-east-1_eZFTqLvVz",
    userPoolWebClientId: "2jq7btif1lilr4np3p4vqc6das",
  },
  Storage: {
    AWSS3: {
      bucket: "",
      region: "us-east-1",
    },
  },
});

export default function Root() {
  return (
    <React.StrictMode>
      <Authenticator.Provider>
        <App />
      </Authenticator.Provider>
    </React.StrictMode>
  );
}
