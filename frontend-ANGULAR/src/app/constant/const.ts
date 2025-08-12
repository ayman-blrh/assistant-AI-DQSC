export interface Question {
    question : string
}
export interface Reponse{
    answer : string
    source_content : string
    source_name : string
}

export interface Ingest {
    chemin : string
}

export interface IngestReponse {
    status : string
    detail : string
}

export const BASE_URL = 'http://localhost:8000/';