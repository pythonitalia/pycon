import React, {Component} from 'react';
import classnames from 'classnames';
import PropTypes from 'prop-types';
import withRipple from '../ripple';

export class Button extends Component {
  render() {
    const {
      className,
      raised,
      unelevated,
      outlined,
      stroked,
      icon,
      children,
      initRipple,
      tagName,
      unbounded, // eslint-disable-line no-unused-vars
      ...otherProps
    } = this.props;

    const classes = classnames('mdc-button', className, {
      'mdc-button--raised': raised,
      'mdc-button--unelevated': unelevated,
      'mdc-button--outlined': outlined,
      'mdc-button--stroked': stroked,
    });

    const Component = tagName || 'button';

    return (
      <Component
        className={classes}
        ref={initRipple}
        {...otherProps}
      >
        {icon ? this.renderIcon() : null}
        {children}
      </Component>
    );
  }

  addClassesToElement(classes, element) {
    const propsWithClasses = {
      className: classnames(classes, element.props.className),
    };
    return React.cloneElement(element, propsWithClasses);
  }

  renderIcon() {
    const {icon} = this.props;
    return this.addClassesToElement('mdc-button__icon', icon);
  }
}

Button.propTypes = {
  raised: PropTypes.bool,
  tagName: PropTypes.string,
  unelevated: PropTypes.bool,
  outlined: PropTypes.bool,
  stroked: PropTypes.bool,
  disabled: PropTypes.bool,
  unbounded: PropTypes.bool,
  initRipple: PropTypes.func,
  className: PropTypes.string,
  icon: PropTypes.element,
  children: PropTypes.string,
};

Button.defaultProps = {
  raised: false,
  unelevated: false,
  outlined: false,
  tagName: 'button',
  stroked: false,
  disabled: false,
  unbounded: false,
  initRipple: () => {},
  className: '',
  icon: null,
  children: '',
};

export default withRipple(Button);
