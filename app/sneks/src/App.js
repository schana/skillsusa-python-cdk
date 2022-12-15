import logo from './logo.svg';
import './App.css';

import { Amplify } from 'aws-amplify';

import { withAuthenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';

//import awsExports from './aws-exports';
//Amplify.configure(awsExports);
Amplify.configure({
    Auth: {
        region: 'us-east-1', // REQUIRED - Amazon Cognito Region
        userPoolId: 'us-east-1_5qPGQ7PVq', //OPTIONAL - Amazon Cognito User Pool ID
        userPoolWebClientId: '5ffs1d5kpodcljl7in0jj771fm',
    }
});

function App({ signOut, user }) {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload, {user.username}.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default withAuthenticator(App);
