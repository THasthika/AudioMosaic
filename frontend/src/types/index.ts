export interface DataSet {
    name: string;
    lables: Lable[];
    file?: File;
}
export interface Lable {
    name: string;
    color: string;
    description: string;
}
export type LableType = 'name' | 'description' | 'color';
