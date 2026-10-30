INSERT INTO society_events
(event_title, description, venue, start_time, end_time, created_by, event_status)
SELECT
'Diwali Community Celebration',
'Community gathering and cultural celebration.',
'Community Hall',
TIMESTAMPTZ '2026-11-08 18:00:00+05:30',
TIMESTAMPTZ '2026-11-08 21:00:00+05:30',
resident_id,
'Planned'
FROM residents
WHERE email = 'diya@example.com';
