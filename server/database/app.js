const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const app = express();

// Imposta la porta da variabile d'ambiente, altrimenti usa 3030
const port = process.env.PORT || 3030;

// Configura middleware
app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));

// Percorsi dei file JSON (modifica qui in base alla tua struttura di cartelle)
const reviews_data = JSON.parse(fs.readFileSync("./database/data/reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("./database/data/dealerships.json", 'utf8'));

// Connessione a MongoDB usando variabile d'ambiente per l'URL
const mongoUrl = process.env.MONGO_URL || "mongodb://root:example@mongo_db:27017/dealershipsDB?authSource=admin";

mongoose.connect(mongoUrl, {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => console.log('Connesso a MongoDB'))
.catch(err => console.error('Errore durante la connessione a MongoDB:', err));

// Importa modelli
const Reviews = require('./review.js');
const Dealerships = require('./dealership.js');

// Popola il database con i dati iniziali
(async () => {
  try {
    await Reviews.deleteMany({});
    await Reviews.insertMany(reviews_data['reviews']);
    
    await Dealerships.deleteMany({});
    await Dealerships.insertMany(dealerships_data['dealerships']);
    console.log("Database popolato con successo.");
  } catch (error) {
    console.error('Errore durante il popolamento del database:', error);
  }
})();

// Rotta principale
app.get('/', (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Rotta per recuperare tutte le recensioni
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Errore durante il recupero delle recensioni' });
  }
});

// Rotta per recuperare recensioni di un dealer specifico
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({ dealership: req.params.id });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Errore durante il recupero delle recensioni per dealer' });
  }
});

// Rotta per recuperare tutti i dealer
// Fetch all dealers
app.get('/fetchDealers', async (req, res) => {
  try {
      const dealers = await Dealerships.find();
      res.json(dealers);
  } catch (error) {
      res.status(500).json({ error: 'Error fetching dealers' });
  }
});

// Fetch dealers by state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
      const dealers = await Dealerships.find({ state: req.params.state });
      res.json(dealers);
  } catch (error) {
      res.status(500).json({ error: 'Error fetching dealers by state' });
  }
});

// Fetch dealer by id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
      const dealer = await Dealerships.findOne({ id: req.params.id });
      res.json(dealer);
  } catch (error) {
      res.status(500).json({ error: 'Error fetching dealer by ID' });
  }
});


// Rotta per inserire una recensione
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  const data = JSON.parse(req.body);
  try {
    const documents = await Reviews.find().sort({ id: -1 });
    let new_id = documents.length ? documents[0]['id'] + 1 : 1;

    const review = new Reviews({
      id: new_id,
      name: data['name'],
      dealership: data['dealership'],
      review: data['review'],
      purchase: data['purchase'],
      purchase_date: data['purchase_date'],
      car_make: data['car_make'],
      car_model: data['car_model'],
      car_year: data['car_year'],
    });

    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Errore durante l\'inserimento della recensione' });
  }
});

// Avvia il server
app.listen(port, () => {
  console.log(`Server attivo su http://localhost:${port}`);
});
