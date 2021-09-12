CREATE TABLE members (
    memberId integer PRIMARY KEY,
    ftId INTEGER,
    firstName TEXT NOT NULL,
    middleName TEXT,
    lastName TEXT NOT NULL,
    photoLocation TEXT NOT NULL,
    bio TEXT
);
CREATE TABLE phoneNumbers (
    phoneId INTEGER PRIMARY KEY, 
    phoneNumber INTEGER NOT NULL,
    memberId INTEGER NOT NULL,
    FOREIGN KEY (memberId)
        REFERENCES members (memberId)
);
CREATE TABLE email (
    mail_id INTEGER PRIMARY KEY,
    email TEXT NOT NULL,
    memberId INTEGER NOT NULL,
    FOREIGN KEY (memberId)
        REFERENCES members (memberId)
);
CREATE TABLE periods (
    periodId INTEGER PRIMARY KEY,
    startDate TEXT NOT NULL,
    endDate TEXT NOT NULL
);
CREATE TABLE memberPeriods (
    memberPeriodId INTEGER PRIMARY KEY,
    memberId INTEGER NOT NULL,
    periodID INTEGER NOT NULL,
    FOREIGN KEY (memberID)
        REFERENCES members (memberId),
    FOREIGN KEY (periodID)
        REFERENCES periods (periodId)
);
CREATE TABLE eductations (
    educationId INTEGER PRIMARY KEY,
    educationLevel INTEGER NOT NULL
);
CREATE TABLE institutionType ( 
    typeId INTEGER PRIMARY KEY,
    typeName TEXT NOT NULL
);

CREATE TABLE institutions (
    institutionId INTEGER PRIMARY KEY,
    institution TEXT NOT NULL,
    typeId INTEGER NOT NULL,
    FOREIGN KEY (typeId)
        REFERENCES institutionType (typeId)
);
CREATE TABLE votingAreaTypes ( 
    areaTypeId INTEGER PRIMARY KEY,
    areaType TEXT NOT NULL
);
CREATE TABLE votingAreas ( 
    areaId INTEGER PRIMARY KEY,
    areaName TEXT NOT NULL,
    areaType TEXT NOT NULL,
    startDate Text NOT NULL,
    endDate TEXT NOT NULL,
    FOREIGN KEY (areaType) 
        REFERENCES votingAreaTypes (areaTypeId)
);
CREATE TABLE pollingPlaces (
    pollingPlaceId INTEGER PRIMARY KEY,
    pollingPlace TEXT NOT NULL,
    votingArea INTEGER NOT NULL,
    startDate TEXT NOT NULL,
    endDate TEXT NOT NULL,
    FOREIGN KEY (votingArea) 
        REFERENCES votingAreas (areaId)
);
CREATE TABLE electionTypes ( 
    electionTypeId INTEGER PRIMARY KEY,
    typeName TEXT NOT NULL
);
CREATE TABLE elections (
    electionId INTEGER PRIMARY KEY,
    electionType TEXT NOT NULL,
    electionDate TEXT NOT NULL,
    FOREIGN KEY (electionType) 
        REFERENCES electionTypes (electionTypeId)
);
CREATE TABLE electionResults ( 
    resultId INTEGER PRIMARY KEY,
    electionId INTEGER NOT NULL,
    pollingPlaceId INTEGER NOT NULL,
    memberId INTEGER NOT NULL,
    votes INTEGER NOT NULL
)
