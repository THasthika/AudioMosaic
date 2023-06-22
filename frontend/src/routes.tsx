import { Routes, Route } from "react-router-dom";
import CreateDataSet from "./components/CreateDataSet";
import ViewDataSets from "./components/ViewDataSets";

function RoutesList() {
    return (
        <Routes>
            <Route path="/" element={<CreateDataSet />} />
            <Route path="/view" element={<ViewDataSets />} />
        </Routes>
    )
}

export default RoutesList