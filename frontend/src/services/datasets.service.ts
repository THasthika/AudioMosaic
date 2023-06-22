import { DataSet } from "@/types";
import { API_URL } from "@/config/index";
import axios from "axios";
import { toast } from 'react-toastify';


export const postDataset = async (dataset: DataSet): Promise<boolean> => {
    try {
        const { data: { id: datasetId } } = await axios.post(`${API_URL}/api/v1/datasets`, { name: dataset.name })
        await axios.post(`${API_URL}/api/v1/labels/${datasetId}`, dataset.lables)
        return true
    } catch (error: any) {
        toast.error(error.response.data.detail || "Something went wrong creating dataset")
        return false
    }
}

export const fetchDatasets = async (): Promise<DataSet[]> => {
    try {
        const { data } = await axios.get(`${API_URL}/api/v1/datasets`)
        return data as DataSet[]
    } catch (error: any) {
        toast.error(error.response.data.detail || "Something went wrong fetching datasets")
        return []
    }
}
