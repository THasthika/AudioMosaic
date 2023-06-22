export interface DataSet {
    id?:string;
    name: string;
    lables: Lable[];
    file?: File;
    created_at?: string;
    updated_at?:string;
}
export interface Lable {
    name: string;
    color: string;
    description: string;
}
export type LableType = 'name' | 'description' | 'color';
