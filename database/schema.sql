-- ---------------------------------------
-- Complaints Table
-- ---------------------------------------

CREATE TABLE IF NOT EXISTS complaints (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    complaint_id TEXT UNIQUE,

    full_name TEXT NOT NULL,

    mobile_number TEXT NOT NULL,

    email TEXT,

    district TEXT NOT NULL,


    -- AI Prediction Fields

    ai_category TEXT,

    department TEXT NOT NULL,

    ai_confidence REAL DEFAULT 0.0,


    -- AI Priority

    priority TEXT DEFAULT 'Medium',


    complaint_title TEXT NOT NULL,

    complaint_description TEXT NOT NULL,


    image_path TEXT,


    status TEXT DEFAULT 'Pending',


    officer_remark TEXT,


    updated_at TIMESTAMP,


    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- ---------------------------------------
-- Officers Table
-- ---------------------------------------

CREATE TABLE IF NOT EXISTS officers (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    username TEXT UNIQUE NOT NULL,

    password TEXT NOT NULL,

    department TEXT NOT NULL,

    role TEXT NOT NULL

);