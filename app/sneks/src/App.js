import {useState} from "react";

import { Amplify } from 'aws-amplify';

import AppLayout from "@cloudscape-design/components/app-layout";

import Content from "./components/content";
import Navigation from "./components/navigation";
import Tools from "./components/tools";
import Notifications from "./components/notifications";

import "@cloudscape-design/global-styles/index.css"
import '@aws-amplify/ui-react/styles.css';
import './App.css';

Amplify.configure({
    Auth: {
        region: 'us-east-1', // REQUIRED - Amazon Cognito Region
        userPoolId: 'us-east-1_5qPGQ7PVq', //OPTIONAL - Amazon Cognito User Pool ID
        userPoolWebClientId: '5ffs1d5kpodcljl7in0jj771fm',
    },
    Storage: {
        AWSS3: {
            bucket: '',
            region: 'us-east-1'
        }
    }
});

/*
import AppLayout from '@awsui/components-react/app-layout';
import { useAppLayout } from 'use-awsui';
import { Breadcrumbs, Content, Navigation, Tools } from './components';

export default function MyApp() {
  const {
    handleNavigationChange,
    handleToolsChange,
    navigationOpen,
    toolsOpen,
  } = useAppLayout({
    defaultNavigationOpen: true,
    defaultToolsOpen: false,
  });

  return (
    <AppLayout
      breadcrumbs={<Breadcrumbs />}
      content={<Content />}
      contentType="table"
      navigation={<Navigation />}
      navigationOpen={navigationOpen}
      onNavigationChange={handleNavigationChange}
      onToolsChange={handleToolsChange}
      tools={<Tools />}
      toolsOpen={toolsOpen}
    />
  );
}
*/

export default function App() {
  const [onToolsToggle] = useState(true);
  return (

  <AppLayout
    toolsOpen={true}
    onToolsChange={({detail}) => onToolsToggle(detail.open)}
    navigation={<Navigation />}
    notifications={<Notifications />}
    tools={<Tools />}
    content={<Content />}
  />

  );
}
