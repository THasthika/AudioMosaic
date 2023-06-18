import { DataSet } from "@/types";
import { API_URL } from "@/config/index";
import axios from "axios";


export const postDataset = async (dataset: DataSet) => {
    try {
        await axios.post(`${API_URL}/api/v1/datasets`, { name: dataset.name })
        // TODO: call other endpoints when the API is ready
    } catch (error) {
        console.log(error)
    }
}
