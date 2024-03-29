import React from 'react';
import { render, screen } from '@testing-library/react';
import Footer from '../components/FormContainer';
import FormContainer from '../components/FormContainer';
import { Container, Row, Col } from 'react-bootstrap';

test('it render Hello', () => {
    const childText = 'Hello';
    render(<FormContainer children={childText} />)
    const text = screen.getByText('Hello');
    expect(text).toBeInTheDocument();
});