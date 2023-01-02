import * as React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import SideNavigation from "@cloudscape-design/components/side-navigation";
import { useAuthenticator } from "@aws-amplify/ui-react";

export default function Navigation() {
  const location = useLocation();
  const [activeHref, setActiveHref] = React.useState(location.pathname);
  const { authStatus } = useAuthenticator((context) => [context.authStatus]);

  React.useEffect(() => {
    setActiveHref(location.pathname);
  }, [location]);
  const navigate = useNavigate();

  const items = [{ type: "link", text: "Home", href: "/" }];

  if (authStatus === "authenticated") {
    items.push(
      { type: "link", text: "Start", href: "/start" },
      { type: "link", text: "Submit", href: "/submit" },
      { type: "link", text: "Submissions", href: "/submissions" }
    );
  }

  items.push(
    { type: "divider" },
    {
      type: "link",
      text: "Submission template",
      href: "/template/template.zip",
      external: true,
    },
    {
      type: "link",
      text: "Documentation",
      href: "/docs/index.html",
      external: true,
    },
    {
      type: "link",
      text: "Inspiration",
      href: "https://youtu.be/L73WY-IT2sE",
      external: true,
    }
  );

  return (
    <SideNavigation
      activeHref={activeHref}
      header={{ href: "/", text: "Navigation" }}
      onFollow={(event) => {
        if (!event.detail.external) {
          event.preventDefault();
          setActiveHref(event.detail.href);
          navigate(event.detail.href);
        }
      }}
      items={items}
    />
  );
}
