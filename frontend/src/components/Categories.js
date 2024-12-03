import React from "react";
import { useSpring, animated } from "react-spring";
import {
  FaBook,
  FaBinoculars,
  FaAtom,
  FaHeart,
  FaHistory,
  FaUtensils,
  FaMagic,
  FaLightbulb,
} from "react-icons/fa";
import "../styles/Home.css";
import { useNavigate } from "react-router-dom";

const categoryIcons = {
  Ficción: <FaBook />,
  Thriller: <FaBinoculars />,
  Ciencia: <FaAtom />,
  Fantasía: <FaMagic />,
  Romance: <FaHeart />,
  Biografías: <FaLightbulb />,
  Historia: <FaHistory />,
  Cocina: <FaUtensils />,
};

const categories = [
  "Ficción",
  "Thriller",
  "Ciencia",
  "Fantasía",
  "Romance",
  "Biografías",
  "Historia",
  "Cocina",
];

function Categories() {
  const fadeIn = useSpring({
    from: { opacity: 0, transform: "translateY(20px)" },
    to: { opacity: 1, transform: "translateY(0)" },
    config: { duration: 500 },
  });

  const navigate = useNavigate();

  const handleCategoryClick = (category) => {
    navigate(`/buscar?filter=Género&query=${encodeURIComponent(category)}`);
  };

  return (
    <section className="section-container">
      <h2 className="section-title">Categorías</h2>
      <div className="category-grid">
        {categories.map((category, index) => (
          <animated.div
            key={index}
            style={fadeIn}
            className="category-card"
            onClick={() => handleCategoryClick(category)}
          >
            <div className="icon-wrapper">{categoryIcons[category]}</div>
            <span className="category-name">{category}</span>
          </animated.div>
        ))}
      </div>
    </section>
  );
}

export default Categories;
