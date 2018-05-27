import React from 'react';
import styled from '../../styled';

const BaseHero = styled.div`
  font-family: ${props => props.theme.fonts.card};
  width: 100%;
  height: 100vh;

  position: relative;
  overflow: hidden;
`;

const HeroBackground = styled.img`
  position: absolute;
  top: 0;
  left: 0;
  object-fit: cover;
  width: 100%;
  height: 100%;
`;

const HeroContent = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 2;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
`;

type Props = {
  srcset?: string;
  sizes?: string;
  src?: string;
};

export class Hero extends React.Component<Props> {
  render() {
    return (
      <BaseHero>
        <HeroContent>{this.props.children}</HeroContent>

        {(this.props.src || this.props.srcset) && (
          <HeroBackground src={this.props.src} srcSet={this.props.srcset} />
        )}
      </BaseHero>
    );
  }
}
