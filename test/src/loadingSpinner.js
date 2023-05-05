import React, { Component } from 'react';
import { usePromiseTracker } from "react-promise-tracker";
import ClipLoader from "react-spinners/ClipLoader";


export const LoadingSpinerComponent = (props) => {
const { promiseInProgress } = usePromiseTracker();

  return (
    <div>
    {
      (promiseInProgress === true) ?
      <div className="show_loading">
      <ClipLoader /></div>

      :
        null
    }
  </div>
  )
};