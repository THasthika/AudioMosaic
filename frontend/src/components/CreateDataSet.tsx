import React from 'react'
import plusIcon from '/src/assets/icons/plus-icon.svg'

interface DataSet {
    name: string;
    labels: Label[];
}
interface Label {
    name: string;
    color: string;
    description: string;
}

const CreateDataSet = () => {
    return (
        <div className='flex flex-col  items-center pt-12'>
            <div className="flex flex flex-col gap-4">
                <input type="text" placeholder="Dataset Name" className="input input-bordered input-primary w-full" />
                <div className="flex items-center gap-4">
                    <label className="input-group">
                        <input type="text" placeholder="Label" className="input input-bordered w-32" />
                        <input type="text" placeholder="Description" className="input input-bordered" />
                        <span><input type="color" /></span>
                    </label>
                    <button className="btn btn-sm btn-circle btn-outline">
                        <img src={plusIcon} alt="plus icon" />
                    </button>
                </div>
            </div>
        </div>
    )
}

export default CreateDataSet