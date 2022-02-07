CREATE TABLE IF NOT EXISTS tasks (
  TaskID VARCHAR PRIMARY KEY,
  TaskDay VARCHAR,
  TaskWeek VARCHAR,
  TaskText VARCHAR,
  TaskMention VARCHAR
);

CREATE TABLE IF NOT EXISTS reminders (
  ReminderID NUMERIC PRIMARY KEY,
  ReminderTime DATE,
  ReminderText VARCHAR,
  ReminderAuthor VARCHAR,
  ReminderChannel VARCHAR
);

CREATE TABLE IF NOT EXISTS actas (
  Persona VARCHAR PRIMARY KEY,
  PersonaMention VARCHAR,
  PersonaCount NUMERIC DEFAULT 0
);
