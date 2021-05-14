import React from "react";
import "./Home.css";
import { Link } from "react-router-dom";
import AppsIcon from "@material-ui/icons/Apps";
import { Avatar } from "@material-ui/core";
import Search from "./Search";
import logo from "../images.png";

function Home() {
  return (
    <div className="home">
      <div className="home-header">
        <div className="home-headerLeft">
        </div>
        <div className="home-headerRight">
        </div>
      </div>
      <div className="home-body">
        <img
          src={logo}
          alt=""
        />
        <div className="home-inputContainer">
          <Search />
        </div>
      </div>
    </div>
  );
}

export default Home;
