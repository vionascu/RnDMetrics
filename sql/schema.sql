CREATE TABLE IF NOT EXISTS snapshots (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  snapshot_date TEXT UNIQUE NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS commit_counts (
  snapshot_id INTEGER NOT NULL,
  date TEXT NOT NULL,
  count INTEGER NOT NULL,
  PRIMARY KEY (snapshot_id, date)
);

CREATE TABLE IF NOT EXISTS loc_totals (
  snapshot_id INTEGER PRIMARY KEY,
  total INTEGER,
  code INTEGER,
  comment INTEGER,
  blank INTEGER
);

CREATE TABLE IF NOT EXISTS test_totals (
  snapshot_id INTEGER PRIMARY KEY,
  count INTEGER
);

CREATE TABLE IF NOT EXISTS file_types (
  snapshot_id INTEGER NOT NULL,
  extension TEXT NOT NULL,
  files INTEGER,
  loc INTEGER,
  PRIMARY KEY (snapshot_id, extension)
);

CREATE TABLE IF NOT EXISTS epic_stats (
  snapshot_id INTEGER NOT NULL,
  epic_key TEXT NOT NULL,
  commits INTEGER,
  loc INTEGER,
  PRIMARY KEY (snapshot_id, epic_key)
);

CREATE TABLE IF NOT EXISTS source_files (
  snapshot_id INTEGER NOT NULL,
  path TEXT NOT NULL,
  loc INTEGER,
  extension TEXT,
  PRIMARY KEY (snapshot_id, path)
);

CREATE TABLE IF NOT EXISTS coverage_totals (
  snapshot_id INTEGER PRIMARY KEY,
  line_rate REAL,
  branch_rate REAL
);
