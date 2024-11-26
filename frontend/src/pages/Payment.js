
import React from 'react';
import { Container, Button, Alert } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

function Payment() {
    const navigate = useNavigate();

    const handlePayment = () => {
        // Aquí puedes integrar la lógica de pago
        // Por ejemplo, enviar los datos al backend para procesar el pago
        alert('Pago procesado exitosamente!');
        navigate('/'); // Redirige al usuario a la página principal después del pago
    };

    return (
        <Container className="mt-4">
            <h2>Procesar Pago</h2>
            <Alert variant="info">
                Aquí puedes integrar tu método de pago preferido.
            </Alert>
            <Button variant="primary" onClick={handlePayment}>
                Realizar Pago
            </Button>
        </Container>
    );
}

export default Payment;