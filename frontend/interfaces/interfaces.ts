export interface Quest {
    embedding: number[];
    title: string;
    link?: string;
    start_time: number;
    end_time: number;
    location: string;
}