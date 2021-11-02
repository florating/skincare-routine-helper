"use strict";

// const e = React.createElement;
const { Button, Form, Grid, Header, Image, Message, Segment } = semanticUIReact

// only needed if no CDN script tag used:
// import React from 'react'
// https://react.semantic-ui.com/usage
// import { Button, Form, Grid, Header, Image, Message, Segment } from 'semantic-ui-react'

const LoginForm = () => {
  console.log("LoginForm is running.");
  return (
  <Grid textAlign='center' style={{ height: '100vh' }} verticalAlign='middle'>
    <Grid.Column style={{ maxWidth: 450 }}>
      <Header as='h2' color='teal' textAlign='center'>
        Log-in to your account
        {/* <Image src='/logo.png' /> Log-in to your account */}
      </Header>
      <Form size='large'>
        <Segment stacked>
          <Form.Input fluid icon='user' iconPosition='left' placeholder='E-mail address' />
          <Form.Input
            fluid
            icon='lock'
            iconPosition='left'
            placeholder='Password'
            type='password'
          />
          <Button color='teal' fluid size='large'>
            Login
          </Button>
        </Segment>
      </Form>
      <Message>
        New to us? <a href='#'>Sign Up</a>
      </Message>
    </Grid.Column>
  </Grid>
  );
};

// const domContainer = document.querySelector('#like_button_container');
// ReactDOM.render(<LoginForm />, domContainer);
ReactDOM.render(<LoginForm />, document.querySelector('#root'));
