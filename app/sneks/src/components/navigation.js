import * as React from "react";
import SideNavigation from "@cloudscape-design/components/side-navigation";
import Badge from "@cloudscape-design/components/badge";

export default () => {
  const [activeHref, setActiveHref] = React.useState("#/");
  return (
    <SideNavigation
      activeHref={activeHref}
      header={{ href: "#/", text: "Sneks" }}
      onFollow={(event) => {
        if (!event.detail.external) {
          event.preventDefault();
          setActiveHref(event.detail.href);
        }
      }}
      items={[
        { type: "link", text: "Results", href: "#/" },
        { type: "link", text: "Submit", href: "#/submit" },
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
};
