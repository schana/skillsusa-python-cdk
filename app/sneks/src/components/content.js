import * as React from "react";
import { useRoutes, Navigate } from "react-router-dom";

import AuthGuard from "./authenticator";
import Home from "./home";
import Start from "./start";
import Submit from "./submit";
import Submissions from "./submissions";

export default function Content({ colorMode }) {
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
      path: "start",
      element: <Start />,
    },
    {
      path: "submit",
      element: <Submit />,
    },
    {
      path: "submissions",
      element: <Submissions colorMode={colorMode} />,
    },
  ]);

  return <>{element}</>;
}
