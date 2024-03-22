import { useState } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { Route, Routes } from 'react-router-dom';
import styled from 'styled-components';

import Home from './pages/home';
import CreateProject from './pages/createproject';

import './App.css';

function App() {

  return (
    <Router>
        <Routes>
          <Route exact path="/" element= {<Home />} />
          <Route exact path="/createproject" element= {<CreateProject />} />
        </Routes>
    </Router>
  );
}

export default App;