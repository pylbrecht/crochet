export interface Auth {
	user_id: string; // uuid
	hash: string;
}

export interface User {
	id: string; // uuid
	username: string;
	email: string;
	name?: string;
	first_name?: string;
}
