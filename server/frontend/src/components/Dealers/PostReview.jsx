import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png";

const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState();
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);

  let curr_url = window.location.href;
  let root_url = curr_url.substring(0, curr_url.indexOf("postreview"));
  let params = useParams();
  let id = params.id;
  let dealer_url = `${root_url}djangoapp/dealer/${id}`; 
  let review_url = `${root_url}djangoapp/add_review/${id}`;

  let carmodels_url =  root_url + `djangoapp/get_cars/`;

  const post_review = async () => {
    let name = sessionStorage.getItem("firstname") + " " + sessionStorage.getItem("lastname");
    if (name.includes("null")) {
      name = sessionStorage.getItem("username");
    }
    if (!model || review === "" || date === "" || year === "" || model === "") {
      alert("All details are mandatory");
      return;
    }
  
    let model_split = model.split(" ");
    let make_chosen = model_split[0];
    let model_chosen = model_split[1];
  
    let jsoninput = JSON.stringify({
      "name": name,
      "dealership": id,  // Associa il dealer_id
      "review": review,
      "purchase": true,
      "purchase_date": date,
      "car_make": make_chosen,
      "car_model": model_chosen,
      "car_year": year,
    });
  
    const res = await fetch(`/djangoapp/add_review/${id}/`, {  // Passa il dealer_id nell'URL
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: jsoninput,
    });
  
    const json = await res.json();
    if (json.status === 200) {
      window.location.href = window.location.origin + "/dealer/" + id;
    }
  }
  

  const get_dealer = async () => {
    const res = await fetch(dealer_url, {
      method: "GET"
    });
    const retobj = await res.json();

    if (retobj.status === 200) {
      let dealerobjs = Array.from(retobj.dealer);
      if (dealerobjs.length > 0)
        setDealer(dealerobjs[0]);
    }
  };

  const get_cars = async () => {
    const res = await fetch(carmodels_url, {
      method: "GET"
    });
    const retobj = await res.json();

    let carmodelsarr = Array.from(retobj.CarModels);
    setCarmodels(carmodelsarr);
  };

  useEffect(() => {
    get_dealer();
    get_cars();
  }, []);

  return (
    <div>
      <Header />
      <div style={{ margin: "5%", textAlign: "center" }}>
        <h1 style={{ color: "darkblue", fontSize: "2em" }}>{dealer.full_name}</h1>
        <h3 style={{ color: "#666" }}>{dealer.city}, {dealer.address}, {dealer.zip}, {dealer.state}</h3>

        <div style={{ marginTop: "20px" }}>
          <textarea
            id='review'
            cols='50'
            rows='5'
            placeholder='Write your review here...'
            onChange={(e) => setReview(e.target.value)}
            style={{ padding: "10px", fontSize: "16px", width: "80%", borderRadius: "8px", border: "1px solid #ccc" }}
          ></textarea>
        </div>

        <div style={{ marginTop: "20px", fontSize: "18px" }}>
          <label>Purchase Date: </label>
          <input type="date" onChange={(e) => setDate(e.target.value)} style={{ padding: "10px", fontSize: "16px", borderRadius: "8px", border: "1px solid #ccc" }} />
        </div>

        <div style={{ marginTop: "20px", fontSize: "18px" }}>
          <label>Car Make & Model: </label>
          <select
            name="cars"
            id="cars"
            onChange={(e) => setModel(e.target.value)}
            style={{ padding: "10px", fontSize: "16px", borderRadius: "8px", border: "1px solid #ccc" }}
          >
            <option value="" selected disabled hidden>Choose Car Make and Model</option>
            {carmodels.map(carmodel => (
              <option value={carmodel.CarMake + " " + carmodel.CarModel}>{carmodel.CarMake} {carmodel.CarModel}</option>
            ))}
          </select>
        </div>

        <div style={{ marginTop: "20px", fontSize: "18px" }}>
          <label>Car Year: </label>
          <input
            type="number"
            onChange={(e) => setYear(e.target.value)}
            max={2023}
            min={2015}
            style={{ padding: "10px", fontSize: "16px", width: "80px", borderRadius: "8px", border: "1px solid #ccc" }}
          />
        </div>

        <div style={{ marginTop: "20px" , textAlign: "center", alignSelf: "center", justifyContent: "center", alignContent: "center", justifyItems: "center", marginLeft: "auto", marginRight: "auto"}}>
          <button
            className='postreview'
            onClick={post_review}
            style={{ padding: "10px 20px", fontSize: "50px", borderRadius: "8px", backgroundColor: "#28a745", color: "white", border: "none" }}
          >
            Post Review
          </button>
        </div>
      </div>
    </div>
  );
};

export default PostReview;
