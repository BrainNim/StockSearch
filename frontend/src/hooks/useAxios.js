import React from 'react'
import { useState, useEffect, useReducer } from 'react';
import axios, { Method, AxiosRequestConfig } from 'axios';

const createFetchOptions = (Method, bodyData) => {
  let config = {
    method: Method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (bodyData) config.data = bodyData;
  return config;
};
function useAxios(Props, initialUrl, methods, bodyData) {
  const [url] = useState(initialUrl);

  const [state, dispatch] = useReducer(requestReducer, {
    isInit: true,
    isLoading: false,
    isSuccess: false,
    isError: false,
    data: null,
  });
  useEffect(() => {
    const fetchData = async () => {
      dispatch({ type: 'FETCH_INIT', payload: null });
      try {
        if (!url) throw new Error(`Error: URL IS NULL`);
        await axios(url, createFetchOptions(methods, bodyData)).then(result =>
          dispatch({ type: 'FETCH_SUCCESS', payload: result.data }),
        );
      } catch (error) {
        console.error(error);
        if (error.response.status === 401)
          console.error('Unauthorized Request');

        dispatch({ type: 'FETCH_FAILURE', payload: null });
      }
    };

    if (!Props) return;
    fetchData();
  }, [url, methods, Props, bodyData]);

  return { ...state };
}

function requestReducer(state, action) {
  switch (action.type) {
    case 'FETCH_INIT':
      return {
        ...state,
        isInit: false,
        isLoading: true,
        isError: false,
      };
    case 'FETCH_SUCCESS':
      return {
        ...state,
        isInit: false,
        isLoading: false,
        isSuccess: true,
        isError: false,
        data: action.payload,
      };
    case 'FETCH_FAILURE':
      return {
        ...state,
        isInit: false,
        isLoading: false,
        isError: true,
      };
    default:
      throw new Error();
  }
}

export default useAxios;
