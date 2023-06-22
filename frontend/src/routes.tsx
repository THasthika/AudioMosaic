import { Routes, Route } from "react-router-dom";
import CreateDataSet from "./components/CreateDataSet";
import Home from "./components/Home";

function RoutesList() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/create" element={<CreateDataSet />} />
        </Routes>
    )
}

export default RoutesList