import * as React from "react";
import { useRoutes, Navigate } from "react-router-dom";

import AuthGuard from "./authenticator";
import Home from "./home";
import Scores from "./scores";
import Submit from "./submit";

export default function Content() {
  const element = useRoutes([
    {
      path: "/",
      element: <Home />,
    },
    {
      path: "signin",
      element: (
        <AuthGuard>
          <Navigate to="/" replace={true} />
        </AuthGuard>
      ),
    },
    {
      path: "scores",
      element: <Scores />,
    },
    {
      path: "submit",
      element: <Submit />,
    },
  ]);

  return <>{element}</>;
}
