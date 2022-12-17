import * as React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import SideNavigation from "@cloudscape-design/components/side-navigation";

export default function Navigation() {
  const location = useLocation();
  const [activeHref, setActiveHref] = React.useState(location.pathname);
  React.useEffect(() => {
    setActiveHref(location.pathname);
  }, [location]);
  const navigate = useNavigate();

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
      items={[
        { type: "link", text: "Home", href: "/" },
        { type: "link", text: "Scores", href: "/scores" },
        { type: "link", text: "Submit", href: "/submit" },
        { type: "divider" },
        {
          type: "link",
          text: "Documentation",
          href: "https://example.com",
          external: true,
        },
      ]}
    />
  );
}
