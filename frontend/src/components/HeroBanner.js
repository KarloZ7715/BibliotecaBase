import React from 'react';
import { useSpring, animated } from 'react-spring';
import { useNavigate } from 'react-router-dom';

function HeroBanner() {
    const fadeIn = useSpring({
        from: { opacity: 0, transform: 'translateY(50px)' },
        to: { opacity: 1, transform: 'translateY(0)' },
        config: { duration: 1000 },
    });

    const navigate = useNavigate();

    const handleSeeMore = () => {
        navigate(`/buscar?filter=Todo&query=`);
    };

    return (
        <div className="banner-container">
            <animated.div style={fadeIn}>
                <div className="banner-content">
                    <h2 className="banner-title">Descubre nuevos mundos</h2>
                    <p className="banner-subtitle">Explora nuestra colección de libros</p>
                    <button className="banner-button" onClick={handleSeeMore}>Ver más</button>
                </div>
            </animated.div>
        </div>
    );
}

export default HeroBanner;
