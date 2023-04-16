-- this file was manually created
INSERT INTO public.users (display_name, email, handle, cognito_user_id)
VALUES
  ('Andrew Brown', 'andrew@example.co', 'andrewbrown' ,'MOCK'),
  ('Andrew Bayko', 'bayko@example.co', 'bayko' ,'MOCK'),
  ('Opeyemi Oginni', 'opeyemi@example.co', 'opeoginni' ,'MOCK'),
  ('First Tester', 'tester@example.co', 'Tester_The_First' ,'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'opeoginni' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )