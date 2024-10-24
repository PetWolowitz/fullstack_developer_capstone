// frontend/src/components/Dealers/Dealer.jsx

import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Header from '../Header/Header';  // Se hai un componente Header
import review_icon from '../assets/reviewbutton.png';  // Importa un'icona di recensione

const Dealer = () => {
  const [dealer, setDealer] = useState({});
  const [reviews, setReviews] = useState([]);
  const [unreviewed, setUnreviewed] = useState(false);
  const { id } = useParams();  // Ottieni l'ID del dealer dai parametri URL
  const dealer_url = `/djangoapp/dealer/${id}`;
  const reviews_url = `/djangoapp/reviews/dealer/${id}`;

  useEffect(() => {

    

    // Funzione per ottenere i dettagli del dealer
    const getDealer = async () => {
      const res = await fetch(dealer_url);
      const data = await res.json();
      if (data.status === 200) {
        setDealer(data.dealer);
      }
    };

    // Funzione per ottenere le recensioni del dealer
    const getReviews = async () => {
      const res = await fetch(reviews_url);
      const data = await res.json();
      if (data.status === 200 && data.reviews.length > 0) {
        setReviews(data.reviews);
      } else {
        setUnreviewed(true);
      }
    };

    getDealer();
    getReviews();
  }, [id]);

  return (
    <div>
      <Header />
      <h1>{dealer.full_name}</h1>
      <p>{dealer.city}, {dealer.state}</p>

      {reviews.length === 0 && unreviewed === false ? (
        <p>Loading reviews...</p>
      ) : unreviewed ? (
        <p>No reviews yet!</p>
      ) : (
        reviews.map(review => (
          <div key={review.id}>
            <p>{review.review}</p>
            <p>{review.name} - {review.car_make} {review.car_model} ({review.car_year})</p>
          </div>
        ))
      )}

      {/* Mostra il bottone per aggiungere una recensione */}
      {sessionStorage.getItem("username") && (
        <a href={`/postreview/${id}`}>
          <img src={review_icon} alt="Post Review" style={{ width: '200px', cursor: 'pointer', height: '100px', margin: '10px' , marginBottom: '10px', marginTop: '10px', marginLeft: '35px', borderRadius: '20px', boxShadow: '0px 1px 8px rgba(0, 0, 0, 0.5)' }} />
        </a>
      )}
    </div>
  );
};

export default Dealer;
