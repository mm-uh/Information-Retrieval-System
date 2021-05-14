import React, { useState } from "react";
import { useStateValue } from "../StateProvider";
import useGoogleSearch from "../useGoogleSearch";
import "./SearchPage.css";
import Response from "../response";
import { Link } from "react-router-dom";
import Search from "./Search";
import SearchResult from "./SearchResult";
import SearchIcon from "@material-ui/icons/Search";
import DescriptionIcon from "@material-ui/icons/Description";
import ImageIcon from "@material-ui/icons/Image";
import LocalOfferIcon from "@material-ui/icons/LocalOffer";
import RoomIcon from "@material-ui/icons/Room";
import MoreVertIcon from "@material-ui/icons/MoreVert";
import ArrowDropDownIcon from "@material-ui/icons/ArrowDropDown";
import { Button, Checkbox } from "@material-ui/core";
import logo from "../images.png";

function SearchPage() {
  const [{ term, relevants }, dispatch] = useStateValue();
  const { data } = useGoogleSearch(term, relevants); // Live API CALL

  return (
    <div className="search-page">
      <div className="searchPage-header">
        <Link to="/">
          <img
            className="searchPage-logo"
            src={logo}
            alt=""
          />
        </Link>

        <div className="searchPage-headerBody">
          <Search hideButtons relevants={data}/>
          <div className="searchPage-options">
            <div className="searchPage-optionsLeft">
              <div className="searchPage-option">
                <SearchIcon />
                <Link to="/all">More results</Link>
              </div>
            </div>
          </div>  
        </div>
      </div>

      {term && (
        <div className="searchPage-results">
          <p className="searchPage-resultCount">
            Results for: {term}
          </p>

          {data?.map((result) => (
            <SearchResult result={result}/>
          ))}
        </div>
      )}
    </div>
  );
}

export default SearchPage;
