import React from 'react';
import "../assets/style.css";
import "../assets/bootstrap.min.css";

const Header = () => {
  const logout = async (e) => {
    e.preventDefault();
    let logout_url = window.location.origin + "/djangoapp/logout";
    const res = await fetch(logout_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
    });

    const json = await res.json();
    if (json.status === "Logged out") {
      let username = sessionStorage.getItem('username');
      sessionStorage.removeItem('username');
      alert("Logging out " + username + "...");
      window.location.href = window.location.origin;
    } else {
      alert("The user could not be logged out.");
    }
  };

  // The default home page items are the login details panel
  let home_page_items = <div></div>;

  // Gets the username in the current session
  let curr_user = sessionStorage.getItem('username');

  // If the user is logged in, show the username and logout option on home page
  if (curr_user !== null && curr_user !== "") {
    home_page_items = (
      <div className="input_panel">
        <span className='username'>{sessionStorage.getItem("username")}</span>
        <button className="nav_item logout-button" onClick={logout}>Logout</button>
      </div>
    );
  }

  return (
    <div>
      <nav className="navbar navbar-expand-lg navbar-light" style={{ backgroundColor: 'rgba(34, 148, 241, 0.932)', height: '1in' }}>
        <div className="container-fluid">
        <img className="img_icon" src="/static/icona_Nav.png" alt="icona_Nav"/> {/* Tag <img> chiuso correttamente */}
          <h2 className="navbar-brand mx-3 text-white" style={{ paddingRight: '5%' }}>Dealerships</h2>

          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarText">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
              <li className="nav-item">
                <a className="nav-link active text-white" style={{ fontSize: 'larger' }} aria-current="page" href="/">Home</a>
              </li>
              <li className="nav-item">
                <a className="nav-link text-white" style={{ fontSize: 'larger' }} href="/about">About Us</a>
              </li>
              <li className="nav-item">
                <a className="nav-link text-white" style={{ fontSize: 'larger' }} href="/contact">Contact Us</a>
              </li>
            </ul>
            <span className="navbar-text">
              <div className="loginlink" id="loginlogout">
                {home_page_items}
              </div>
            </span>
          </div>
        </div>
      </nav>
    </div>
  );
};

export default Header;
