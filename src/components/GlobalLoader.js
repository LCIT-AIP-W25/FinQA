import React from "react";
import { useLoader } from "./LoaderContext";

const GlobalLoader = () => {
  const { loading } = useLoader();

  if (!loading) return null;

  return (
    <div className="global-loader-overlay">
      <div className="global-loader"></div>
      <p className="loader-text">Processing...</p>
    </div>
  );
};

export default GlobalLoader;
