import { useState, useEffect } from "react";


const useGoogleSearch = (term, previousData) => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      console.log("hello");
      const relevants = previousData?.
                        filter((item) => item.relevant).
                        map((item) => item.index);
      
      console.log(relevants);
      
      const irrelevants = previousData?.
                          filter(item => !item.relevant).
                          map(item => item.index);
      // console.log(relevants)
      const requestOptions = {
        method : 'POST',
        headers : {'Content-Type' : 'application/json'},
        body : JSON.stringify({
          'data' : term,
          'relevants' : (relevants || []), 
          'irrelevants' : (irrelevants || []),
        }),
      }
      const response = await fetch('http://127.0.0.1:5000/query', requestOptions);
      const data = await response.json();
      console.log(data.map(item => item.index));
      const dataToRender = data?.map((item) => { return {
        index: item.index,
        abstract: item.abstract,
        title: item.title,
        relevant: false,
      }})
      setData(dataToRender); 
    };

    fetchData()
      .then((res) => {
        console.log(res);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [term, previousData]);

  return { data };
};

export default useGoogleSearch;
