import * as React from "react";
import { useRoutes } from "react-router-dom";

import HelpPanel from "@cloudscape-design/components/help-panel";
import Button from "@cloudscape-design/components/button";
import { useAuthenticator } from "@aws-amplify/ui-react";

import HomeHelp from "./home-help";
import SignInHelp from "./sign-in-help";

export default function Tools() {
  const { authStatus } = useAuthenticator((context) => [context.authStatus]);
  const placeholder = (
    <p>Reach out to your contest coordinator with any questions.</p>
  );

  const element = useRoutes([
    {
      path: "/",
      element: <HomeHelp />,
    },
    {
      path: "signin",
      element: <SignInHelp />,
    },
    {
      path: "start",
      element: authStatus !== "authenticated" ? <SignInHelp /> : placeholder,
    },
    {
      path: "submit",
      element: authStatus !== "authenticated" ? <SignInHelp /> : placeholder,
    },
    {
      path: "submissions",
      element: authStatus !== "authenticated" ? <SignInHelp /> : placeholder,
    },
  ]);

  return (
    <HelpPanel
      footer={
        <Button
          iconName="envelope"
          iconAlign="right"
          href="mailto:admin@sneks.dev"
        >
          Email the admin
        </Button>
      }
      header={<h2>Additional info</h2>}
    >
      {element}
    </HelpPanel>
  );
}
