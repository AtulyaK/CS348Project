table - login
Hash index on Userrname
The application frequently looks up users by username, especially during login or user registration. Indexing this column speeds up searches and ensures username uniqueness checks are efficient.

table - schedule and class
B+ tree index on date, and userID
Schedule records are often filtered by date to show upcoming classes and grouped or filtered by userID (instructor or admin). Indexing both columns improves query performance for these common operations.
Queries regularly access classes by date (e.g., most recent classes) and by instructor (userID). A compound index supports fast lookups and ordering for this data.

table - availability
B+ tree index on date, and levelID
Availability records are typically filtered by date and level (e.g., to match a student’s level). Indexing these fields accelerates the rendering of available time slots and reduces planning lag.


Concurrency:
| Table          | Recommended Isolation Level        | Justification                           |
| -------------- | ---------------------------------- | --------------------------------------- |
| `Schedule`     | `READ COMMITTED`                   | Lightweight concurrency, no dirty reads |
| `CLASS`        | `REPEATABLE READ`                  | Stable reads for reports/grades         |
| `Availability` | `READ COMMITTED`                   | Fast reads, tolerable staleness         |
| `Competition`  | `READ UNCOMMITTED`                 | Strict edits by admin only              |
| `login`        | `READ COMMITTED`                   | Fast logins with no dirty reads         |