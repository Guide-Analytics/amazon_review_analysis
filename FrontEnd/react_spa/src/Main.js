import React, { Component } from "react";
import {
  Route,
  NavLink,
  HashRouter
} from "react-router-dom";
import Home from "./Home";
import Graph1 from "./Graph1";
import Graph2 from "./Graph2";

class Main extends Component {
  render() {
    return (
      <HashRouter>
        <div>
          <h1>Gide Dashboard</h1>
          <ul className="header">
            <li><NavLink exact to="/">Home</NavLink></li>
            <li><NavLink to="/Graph1">Graph 1</NavLink></li>
            <li><NavLink to="/Graph2">Graph 2</NavLink></li>
          </ul>
          <div className="content">
            <Route path="/" component={Home}/>
            <Route path="/Graph1" component={Graph1}/>
            <Route path="/Graph2" component={Graph2}/>
          </div>
        </div>
      </HashRouter>
    );
  }
}


export default Main;
