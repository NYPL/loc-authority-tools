CREATE SCHEMA IF NOT EXISTS loc_authority_tools;

CREATE TABLE IF NOT EXISTS loc_authority_tools.mads_authority_record (
  uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  record_hash TEXT UNIQUE NOT NULL,
  record TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS loc_authority_tools.loc_person_authority (
  uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  record_source UUID NOT NULL REFERENCES loc_authority_tools.mads_authority_record (uuid),
  loc_url TEXT NOT NULL,
  authoritative_label TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS loc_authority_tools.loc_person_authority_label_token (
  uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  authority_uuid UUID NOT NULL REFERENCES loc_authority_tools.loc_person_authority (uuid),
  token TEXT NOT NULL,
  UNIQUE (authority_uuid, token)
);

CREATE INDEX IF NOT EXISTS token_idx ON loc_authority_tools.loc_person_authority_label_token (token);
