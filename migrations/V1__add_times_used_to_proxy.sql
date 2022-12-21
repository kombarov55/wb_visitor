alter table proxy
add column times_used_for_auth int,
add column auth_blocked_datetime timestamp,
add column last_authenticated_datetime timestamp;
