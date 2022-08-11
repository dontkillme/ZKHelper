export interface ParticipantTshirt {
	id: number;
	size: string;
	givenOut: boolean;
	extra: string | null;
}

export interface ParticipantQuest {
	id: number;
	participantId: number;
	questId: number;
	notes: string | null;
	startedAt: string;
	doneAt: string | null;
	done: boolean;
}

export interface Participant {
	id: number;
	name: string;
	surname: string;
	nick: string;
	phone: string;
	icePhone: string;
	iceName: string;
	iceExtra: string;
	isStaff: boolean;
	accredited: boolean;
	tshirt: ParticipantTshirt[];
	quests: ParticipantQuest[];
}

export interface Quest {
	id: number;
	name: string;
	description: string;
	reward: number;
}
