import plusIcon from '@/assets/icons/plus-icon.svg'
import trashIcon from '@/assets/icons/trash-icon.svg'
import { validateUploadedFile } from '@/helpers/validate-upload-file';
import { useState } from 'react';

interface DataSet {
    name: string;
    lables: Lable[];
    file?: File;
}
interface Lable {
    name: string;
    color: string;
    description: string;
}
type LableType = 'name' | 'description' | 'color';


const CreateDataSet = () => {
    const defaultColor = '#036FE2'
    const [dataSet, setDataSet] = useState<DataSet>({
        name: '',
        lables: [
            {
                name: '',
                color: defaultColor,
                description: ''
            }
        ]
    })

    const onChangeDataSetName = (e: React.ChangeEvent<HTMLInputElement>): void => {
        setDataSet({
            ...dataSet,
            name: e.target.value
        })

    }

    const onChangeDataSetLable = (e: React.ChangeEvent<HTMLInputElement>, index: number): void => {
        const property: LableType = e.target.name as LableType;
        dataSet.lables[index][property] = e.target.value;
        setDataSet({
            ...dataSet,
            lables: [...dataSet.lables]
        })

    }
    const handleAddNewLable = (): void => {
        setDataSet({
            ...dataSet,
            lables: [...dataSet.lables, {
                name: '',
                color: defaultColor,
                description: ''
            }
            ]
        })
    }

    const handleDeleteLable = (index: number): void => {
        if (dataSet.lables.length === 1) return
        const modifiedLables = dataSet.lables.filter((_, idx) => idx !== index)
        setDataSet({
            ...dataSet,
            lables: modifiedLables
        })
    }

    const handleUploadFile = (e: React.ChangeEvent<HTMLInputElement>)=>{
        const file: File = e.target.files![0]
        if(!validateUploadedFile(file)){
            // TODO: Replace with error handling
            console.log("File validation failed");
            return
        }
        setDataSet({
            ...dataSet,
            file
        })
    }

    const handleOnSubmit = () => {
        console.log(dataSet);
    }

    return (
        <div className='flex flex-col  items-center pt-12'>
            <h2 className='text-2xl'>Create new dataset</h2>
            <div className="flex flex flex-col gap-4 mt-12">
                <input type="text" placeholder="Dataset Name" className="input input-bordered input-primary w-full" value={dataSet.name} onChange={onChangeDataSetName} />
                {dataSet?.lables.map((label, index) =>
                (
                    < div className="flex items-center gap-4" key={index} >
                        <label className="input-group">
                            <input type="text" placeholder="Lable" className="input input-bordered w-32" value={label.name} onChange={(e) => onChangeDataSetLable(e, index)} name="name" />
                            <input type="text" placeholder="Description" className="input input-bordered" value={label.description} onChange={(e) => onChangeDataSetLable(e, index)} name="description" />
                            <span><input type="color" value={label.color} onChange={(e) => onChangeDataSetLable(e, index)} name="color" /></span>
                        </label>
                        <button className="btn btn-sm btn-circle btn-outline">
                            <img className="w-4" src={plusIcon} alt="plus icon" onClick={handleAddNewLable} />
                        </button>
                        <button className="btn btn-sm btn-circle btn-outline">
                            <img className="w-4" src={trashIcon} alt="trash icon" onClick={() => handleDeleteLable(index)} />
                        </button>

                    </div>
                )
                )}
                <div>
                    <label className="label">
                        <span className="label-text">Upload audio file</span>
                    </label>
                    <input type="file" className="file-input file-input-bordered w-full" accept=".mp3, .wav" onChange={handleUploadFile}/>
                </div>
            </div>
            <button className='btn mt-8' onClick={handleOnSubmit}>Save</button>
        </div >
    )
}

export default CreateDataSet