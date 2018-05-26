import React from 'react';

interface TitleProps {
  level: 1 | 2 | 3 | 4 | 5 | 6;
  children: React.ReactNode;
}

export const Title = ({ level, children }: TitleProps) => {
  const Component = `h${level}`;

  return (
    <Component className={`mdc-typography mdc-typography--headline${level}`}>
      {children}
    </Component>
  );
};

type ParagraphProps = {
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
};

export const Paragraph: React.SFC<ParagraphProps> = ({ variant, children }) => {
  const level = variant === 'primary' ? 1 : 2;

  return (
    <p className={`mdc-typography mdc-typography--body${level}`}>{children}</p>
  );
};

Paragraph.defaultProps = {
  variant: 'primary',
};
