import { fetchDatasets } from "@/services/datasets.service"
import { DataSet } from "@/types"
import { useEffect, useState } from "react"

function ViewDataSets() {
  const [datasets, setDatasets] = useState<DataSet[]>()
  useEffect(() => {
    fetchDatasets().then((dataset) => {
      setDatasets(dataset)
    })
  }, [])

  return (
    <div className="flex flex-col items-center">
      <h1 className="text-2xl">Your Dataset</h1>
      <div className="overflow-x-auto py-8">
        <table className="table table-zebra">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Created At</th>
              <th>Updated At</th>
            </tr>
          </thead>
          <tbody>
            {datasets?.map(dataset => {
              return (
                <tr key={dataset.id}>
                  <th>{dataset.id}</th>
                  <td>{dataset.name}</td>
                  <td>{dataset.created_at}</td>
                  <td>{dataset.updated_at}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
        <div className="flex justify-center mt-4 join">
          <button className="join-item btn btn-active">1</button>
          <button className="join-item btn">2</button>
        </div>
      </div>
    </div>
  )
}

export default ViewDataSets