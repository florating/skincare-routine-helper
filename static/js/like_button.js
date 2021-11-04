'use strict';

const e = React.createElement;
// const { Button, Icon, Label } = semanticUIReact

class LikeButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {
    if (this.state.liked) {
      return 'You liked this.';
    }

    return e(
      'button',
      { onClick: () => this.setState({ liked: true }) },
      'Like'
    );
  }
}

const domContainer = document.querySelector('#like_button_container');
ReactDOM.render(e(LikeButton), domContainer);


// const domContainer = document.querySelector('#like_button_container')

// // 💡 This example is simplied to use React without JSX
// //    https://reactjs.org/docs/react-without-jsx.html

// // https://reactjs.org/docs/add-react-to-a-website.html#add-react-in-one-minute
// ReactDOM.render(e(Button, { primary: true }, 'Hello world!'), domContainer)
