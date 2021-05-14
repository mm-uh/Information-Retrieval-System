import React, { useEffect, useState } from 'react';
import "./SearchPage.css";
import { Checkbox } from "@material-ui/core";
import { ContactSupportOutlined } from '@material-ui/icons';

const SearchResult = ({result}) => {
    const [relevant, setRelevant] = useState(false);

    useEffect(() => {
        setRelevant(result.relevant);
    })


    return (
        <div className="resultWithRelevant">
            <div className="searchPage-result">
            <a className="searchPage-resultTitle">
                <h2>{result.title}</h2>
            </a>
            <p className="sitemearchPage-resultSnippet">{result.abstract}...</p>
            </div>
            <div className="relevantCheckMark">
            <Checkbox color='default' checked={result.relevant} onChange={() => {
                result.relevant = !relevant;
                setRelevant(!relevant);
            }}/>
            </div>
        </div>
    )
}

export default SearchResult;