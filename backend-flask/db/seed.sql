-- this file was manually created
INSERT INTO public.users (display_name, email, handle, cognito_user_id)
VALUES
  ('Andrew Brown', 'andrew@example.co', 'andrewbrown' ,'MOCK'),
  ('Andrew Bayko', 'bayko@example.co', 'bayko' ,'MOCK'),
  ('Opeyemi Oginni', 'opeyemi@example.co', 'opeoginni' ,'MOCK'),
  ('Another Guy', 'bejanax822@akoption.com', 'this_guy' ,'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'opeoginni' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  ),
  (
    (SELECT uuid from public.users WHERE users.handle = 'this_guy' LIMIT 1),
    'No Its Not!',
    current_timestamp + interval '10 day'
  ),
  (
    (SELECT uuid from public.users WHERE users.handle = 'opeoginni' LIMIT 1),
    'It sure is!',
    current_timestamp + interval '10 day'
  );