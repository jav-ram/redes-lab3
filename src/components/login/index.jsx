import React from 'react';
import * as client from '../../xmpp/client';

class LoginForm extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      user: '',
      password: '',
    };
  }

  handleUser = (e) => {
    this.setState({user: e.target.value});
  }

  handlePassword = (e) => {
    this.setState({password: e.target.value});
  }

  render() {
      return (
        <form>
          <input
            type="text"
            placeholder="User"
            value={this.state.user}
            onChange={this.handleUser}
          />
          <input
            type="password"
            placeholder="Password"
            value={this.state.password}
            onChange={this.handlePassword}
          />
          <button type="button" onClick={ (e) => {
            client.initialize(
              this.state.user,
              this.state.password,
              client.onConnect,
            );
          } }>Login</button>
        </form>
      );
  }
}


export default LoginForm;